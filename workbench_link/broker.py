"""Profile-owned broker. Only private IPC accepts native execution envelopes."""

import fcntl
import http.server
import ipaddress
import os
import socket
import socketserver
import sqlite3
import threading
import time

from . import auth, control, protocol as p
from .errors import Code, LinkError
from .ledger import Ledger
from .store import Store

LEASE_SECONDS = 15


class BoundedThreads(socketserver.ThreadingMixIn):
    daemon_threads = True
    block_on_close = False

    def process_request(self, request, address):
        if not self.capacity.acquire(blocking=False):
            request.close()
            return
        try:
            super().process_request(request, address)
        except BaseException:
            self.capacity.release()
            raise

    def process_request_thread(self, request, address):
        try:
            super().process_request_thread(request, address)
        finally:
            self.capacity.release()

    def handle_error(self, request, address):
        # Handler payloads may contain project data: never emit a traceback.
        pass


class PrivateServer(BoundedThreads, socketserver.UnixStreamServer):
    def __init__(self, path, broker):
        self.capacity = threading.BoundedSemaphore(16)
        self.broker = broker
        super().__init__(str(path), PrivateHandler)


class PrivateHandler(socketserver.BaseRequestHandler):
    def handle(self):
        deadline = time.monotonic() + 3
        try:
            control.check_peer(self.request)
            args = control.receive(self.request, deadline)
            result = self.server.broker.dispatch_control(args)
        except LinkError as exc:
            result = exc.as_dict()
        except sqlite3.Error:
            result = LinkError(Code.STORAGE_UNAVAILABLE, 'Durable ledger is unavailable; execution refused.').as_dict()
        except (OSError, ValueError, TimeoutError, ConnectionError):
            return
        try:
            control.send(self.request, result, deadline)
        except (OSError, TimeoutError):
            pass


class WorkerServer(BoundedThreads, http.server.HTTPServer):
    def __init__(self, address, broker):
        self.capacity = threading.BoundedSemaphore(32)
        self.work_capacity = threading.BoundedSemaphore(12)
        self.broker = broker
        super().__init__(address, WorkerHandler)


class WorkerHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.0'

    def setup(self):
        super().setup()
        self.connection.settimeout(2)

    def log_message(self, *args):
        pass

    def handle_one_request(self):
        # Include request-line/header parsing in the wall-clock read bound.
        def expire():
            try:
                self.connection.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
        timer = threading.Timer(3, expire)
        timer.daemon = True
        timer.start()
        try:
            super().handle_one_request()
        finally:
            timer.cancel()

    def do_POST(self):
        work_slot = False
        try:
            if self.path not in auth.PATHS:
                p.bad('Unsupported worker path.')
            for name in ('Content-Length', 'Transfer-Encoding', *auth.HEADERS):
                if len(self.headers.get_all(name, [])) > 1:
                    p.bad('Duplicate transport header.')
            if self.headers.get('Transfer-Encoding') is not None:
                p.bad('Chunked requests are unsupported.')
            length = self.headers.get('Content-Length', '')
            if not length.isascii() or not length.isdecimal() or len(length) > 8:
                p.bad('A bounded Content-Length is required.')
            length = int(length)
            if not 1 <= length <= p.WIRE_LIMIT:
                p.bad('Worker request exceeds the wire limit.')
            if self.path not in ('/v1/worker/heartbeat', '/v1/worker/result', '/v1/worker/recover'):
                work_slot = self.server.work_capacity.acquire(blocking=False)
                if not work_slot:
                    self.reply(429, {'ok': False, 'code': 'WORKSPACE_BUSY', 'message': 'Worker request capacity reached.', 'operation_id': None})
                    return
            # Raw socket reads avoid an unbounded buffering/readline phase for the body.
            deadline = time.monotonic() + 2
            body = bytearray()
            while len(body) < length:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError
                self.connection.settimeout(remaining)
                part = self.rfile.read1(min(65536, length - len(body)))
                if not part:
                    raise ConnectionError
                body.extend(part)
            broker = self.server.broker
            _, instance_id = auth.verify(broker.key, broker.worker_id, 'POST', self.path,
                                         self.headers, bytes(body), broker.store.consume_nonce)
            args = p.decode(bytes(body))
            self.reply(200, broker.dispatch_worker(self.path.rsplit('/', 1)[1], instance_id, args))
        except LinkError as exc:
            status = 401 if exc.code == Code.AUTH_FAILED else 400 if exc.code == Code.BAD_REQUEST else 503 if exc.code == Code.STORAGE_UNAVAILABLE else 409
            self.reply(status, exc.as_dict())
        except sqlite3.Error:
            self.reply(503, LinkError(Code.STORAGE_UNAVAILABLE, 'Durable ledger is unavailable; execution refused.').as_dict())
        except (OSError, TimeoutError, ConnectionError):
            pass
        finally:
            if work_slot:
                self.server.work_capacity.release()

    def reply(self, status, obj):
        data = p.canonical(obj)
        try:
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Connection', 'close')
            self.end_headers()
            self.wfile.write(data)
        except OSError:
            pass
        self.close_connection = True


class Broker:
    def __init__(self, settings, key, address=('127.0.0.1', 8765), *, local_test=False, tls_context=None):
        if not local_test and tls_context is None:
            raise LinkError(Code.AUTH_FAILED, 'Configure HTTPS; plain HTTP is available only in explicit loopback tests.')
        if local_test and not ipaddress.ip_address(address[0]).is_loopback:
            p.bad('Local-test listener must use literal loopback.')
        self.settings, self.key, self.worker_id = settings, key, settings.worker_id
        self.store = Store(settings.control_dir)
        self.ledger = Ledger(self.store)
        self.stop_event = threading.Event()
        self.heartbeat_lock = threading.Lock()
        self.heartbeats = {}
        self.threads = []
        self.lock_fd = None
        self.private = self.http = None
        try:
            path = self.store.root / 'broker.lock'
            self.lock_fd = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
            try:
                fcntl.flock(self.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise LinkError(Code.WORKSPACE_BUSY, 'A broker already owns this profile.') from None
            socket_path = self.store.root / 'control.sock'
            if socket_path.exists() or socket_path.is_symlink():
                if socket_path.is_symlink() or not socket_path.is_socket() or socket_path.stat().st_uid != os.getuid():
                    raise LinkError(Code.STORAGE_UNAVAILABLE, 'Refusing to replace a control path with unexpected ownership/type.')
                # Exclusive flock is held. Probe to reject a live socket from a nonconforming owner.
                probe = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                probe.settimeout(.2)
                try:
                    probe.connect(str(socket_path))
                except ConnectionRefusedError:
                    socket_path.unlink()
                else:
                    raise LinkError(Code.WORKSPACE_BUSY, 'An existing control socket still answers; refusing takeover.')
                finally:
                    probe.close()
            self.ledger.recover_startup()
            self.private = PrivateServer(socket_path, self)
            os.chmod(socket_path, 0o600)
            self.http = WorkerServer(address, self)
            if tls_context:
                self.http.socket = tls_context.wrap_socket(self.http.socket, server_side=True)
        except BaseException:
            self.close()
            raise

    def start(self):
        for target in (lambda: self.private.serve_forever(poll_interval=.1),
                       lambda: self.http.serve_forever(poll_interval=.1), self._leases):
            thread = threading.Thread(target=target, daemon=True)
            self.threads.append(thread); thread.start()
        return self

    def _leases(self):
        while not self.stop_event.wait(.25):
            with self.heartbeat_lock:
                expired = [instance for instance, last in self.heartbeats.items() if time.monotonic() - last > LEASE_SECONDS]
                for instance in expired:
                    del self.heartbeats[instance]
            for instance in expired:
                self.ledger.disconnect(instance)

    def _connected(self, instance):
        with self.heartbeat_lock:
            return time.monotonic() - self.heartbeats.get(instance, float('-inf')) <= LEASE_SECONDS

    def dispatch_control(self, args):
        action = args.get('action')
        if action == 'status':
            p.fields(args, {'action'})
            status = self.ledger.status()
            status['connected'] = bool(status['binding'] and self._connected(status['binding']['instance_id']))
            return status
        if action == 'bind':
            p.fields(args, {'action', 'instance_id', 'project_id', 'image'})
            if not self._connected(args['instance_id']):
                raise LinkError(Code.WORKER_UNAVAILABLE, 'Registered worker is disconnected.')
            return dict(self.ledger.bind(args['instance_id'], args['project_id'], args['image']), ok=True)
        if action == 'open_environment':
            p.fields(args, {'action'})
            binding = self.ledger.status()['binding']
            if not binding or not self._connected(binding['instance_id']):
                raise LinkError(Code.WORKER_UNAVAILABLE, 'Accepted worker is disconnected; execution refused.')
            return dict(self.ledger.open_environment(), ok=True)
        if action == 'submit':
            p.fields(args, {'action', 'envelope'})
            envelope = p.envelope(args['envelope'])
            if not self._connected(envelope['worker_instance_id']):
                # Existing uncertain IDs remain recoverable even while disconnected.
                try:
                    return self.ledger.operation(envelope['operation_id'])
                except LinkError:
                    raise LinkError(Code.WORKER_UNAVAILABLE, 'Worker is disconnected; operation was not queued.') from None
            return self.ledger.submit(envelope)
        if action in ('operation_status', 'cancel'):
            p.fields(args, {'action', 'operation_id'})
            return self.ledger.operation(args['operation_id']) if action == 'operation_status' else self.ledger.cancel(args['operation_id'])
        if action == 'read_output':
            p.fields(args, {'action', 'operation_id', 'offset'})
            return {'ok': True, 'data_b64': p.b64(self.ledger.read_output(args['operation_id'], args['offset']))}
        if action == 'close_environment':
            p.fields(args, {'action', 'environment_id'})
            return self.ledger.close_environment(args['environment_id'])
        p.bad('Unsupported private control action.')

    def dispatch_worker(self, action, instance, args):
        if action == 'hello':
            p.fields(args, {'protocol_version', 'project_id', 'alias', 'image', 'capabilities'})
            p.integer(args['protocol_version'], 'protocol_version', 1, 1)
            result = self.ledger.hello(self.worker_id, instance, args['project_id'], args['alias'], args['image'], args['capabilities'])
            with self.heartbeat_lock:
                self.heartbeats[instance] = time.monotonic()
            return result
        if action == 'heartbeat':
            p.fields(args, {'binding_id', 'generation', 'active_operation_id'})
            binding = self.ledger.status()['binding']
            if binding and (binding['instance_id'], binding['binding_id'], binding['generation']) != (instance, args['binding_id'], args['generation']):
                raise LinkError(Code.BINDING_STALE, 'Heartbeat cannot renew another binding generation.')
            if not binding and (args['binding_id'] is not None or args['generation'] is not None):
                p.bad('Unbound heartbeat identity must be null.')
            with self.heartbeat_lock:
                self.heartbeats[instance] = time.monotonic()
            cancel = binding is not None and binding['state'] != 'ACTIVE'
            if args['active_operation_id'] is not None:
                op = self.ledger.operation(args['active_operation_id'])
                cancel = cancel or op['cancel_requested']
            return {'ok': True, 'lease_seconds': LEASE_SECONDS, 'cancel_requested': cancel}
        if action == 'poll':
            p.fields(args, set())
            return self.ledger.poll(instance)
        if action in ('accept', 'running'):
            required = {'operation_id', 'payload_sha256'} | ({'start_grant_id'} if action == 'running' else set())
            p.fields(args, required)
            p.identifier(args['operation_id']); p.hash_field(args['payload_sha256'])
            if action == 'accept':
                if not self._connected(instance):
                    raise LinkError(Code.WORKER_UNAVAILABLE, 'No live lease; grant refused.')
                return self.ledger.accept(instance, args['operation_id'], args['payload_sha256'])
            return self.ledger.running(instance, args['operation_id'], args['payload_sha256'], p.identifier(args['start_grant_id']))
        if action == 'output':
            p.fields(args, {'operation_id', 'sequence', 'offset', 'data_b64', 'sha256'})
            return self.ledger.output(instance, args['operation_id'], args['sequence'], args['offset'],
                                      p.unb64(args['data_b64'], p.CHUNK_LIMIT), args['sha256'])
        if action == 'result':
            return self.ledger.result(instance, args)
        if action == 'recover':
            p.fields(args, {'operation_ids'})
            if type(args['operation_ids']) is not list or len(args['operation_ids']) > 32:
                p.bad('Recovery request exceeds the limit.')
            operations = []
            with self.store.lock:
                for identifier in args['operation_ids']:
                    op = self.ledger._op(identifier)
                    if self.ledger._binding(op['binding_id'])['instance_id'] != instance:
                        raise LinkError(Code.BINDING_STALE, 'Recovery instance does not own operation.')
                    operations.append(self.ledger.operation(identifier))
            return {'ok': True, 'operations': operations}
        p.bad('Unsupported worker action.')

    def close(self):
        self.stop_event.set()
        if self.threads:
            for server in (self.http, self.private):
                if server:
                    server.shutdown()
            for thread in self.threads:
                thread.join(2)
        for server in (self.http, self.private):
            if server:
                server.server_close()
        if self.private:
            (self.store.root / 'control.sock').unlink(missing_ok=True)
        if self.lock_fd is not None:
            os.close(self.lock_fd); self.lock_fd = None
        self.store.close()
