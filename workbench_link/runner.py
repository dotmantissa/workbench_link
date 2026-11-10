"""Container-only runner. Control JSON and shell stdin use different pipes.

The container lease is a fail-stop mechanism, not a security boundary against
hostile code running as the same user inside this explicitly selected container.
"""

import hashlib
import os
import select
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

from . import protocol as p


class Runner:
    def __init__(self):
        self.lock = threading.Lock()
        self.cancel = threading.Event()
        self.last_renewal = time.monotonic()
        self.active = None
        self.stop = threading.Event()

    def emit(self, obj):
        with self.lock:
            sys.stdout.buffer.write(p.canonical(obj) + b'\n')
            sys.stdout.buffer.flush()

    def children(self):
        # /proc is private to this container; no host PID namespace is mounted.
        return [int(path.name) for path in Path('/proc').iterdir()
                if path.name.isdecimal() and int(path.name) not in (1, os.getpid())]

    def terminate_children(self):
        for signum, grace in ((signal.SIGTERM, 2), (signal.SIGKILL, 1)):
            for pid in self.children():
                try:
                    os.kill(pid, signum)
                except ProcessLookupError:
                    pass
            deadline = time.monotonic() + grace
            while self.children() and time.monotonic() < deadline:
                # Reap adopted children (the runner is container PID 1).
                try:
                    while os.waitpid(-1, os.WNOHANG)[0]:
                        pass
                except ChildProcessError:
                    pass
                time.sleep(.02)
            if not self.children():
                return 'group_term' if signum == signal.SIGTERM else 'group_kill'
        return None

    def run(self, envelope, grant):
        started = time.monotonic()
        operation_id = envelope['operation_id']
        digest = hashlib.sha256()
        output_bytes = sequence = 0
        cancelled = False
        complete = True
        method = 'natural'
        exit_code = None
        script_path = None
        try:
            fd, script_path = tempfile.mkstemp(prefix='workbench-script-', dir='/tmp')
            with os.fdopen(fd, 'wb') as script:
                script.write(envelope['script'].encode('utf-8'))
            command = ['bash', '-l' if envelope['login'] else '--noprofile', script_path]
            # No environment from Hermes or the worker daemon is forwarded.
            process = subprocess.Popen(command, cwd='/workspace', env={
                'PATH': '/usr/local/bin:/usr/bin:/bin', 'HOME': '/tmp', 'LANG': 'C.UTF-8'},
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
            self.emit({'kind': 'running', 'operation_id': operation_id})
            raw_stdin = p.unb64(envelope['stdin_b64'], p.STDIN_LIMIT)

            def input_writer():
                try:
                    process.stdin.write(raw_stdin); process.stdin.flush()
                except (BrokenPipeError, OSError):
                    pass
                finally:
                    process.stdin.close()
            writer = threading.Thread(target=input_writer, daemon=True)
            writer.start()
            os.set_blocking(process.stdout.fileno(), False)
            while True:
                if self.cancel.is_set() or time.monotonic() - started >= envelope['timeout_seconds'] or self.stop.is_set():
                    cancelled = True
                    try:
                        os.killpg(process.pid, signal.SIGTERM)
                        process.wait(timeout=2)
                        method = 'group_term'
                    except subprocess.TimeoutExpired:
                        os.killpg(process.pid, signal.SIGKILL); process.wait(timeout=1)
                        method = 'group_kill'
                    except ProcessLookupError:
                        process.wait(timeout=1)
                    # Drain what was produced before termination.
                    self.cancel.clear()
                ready, _, _ = select.select([process.stdout], [], [], .05)
                if ready:
                    data = os.read(process.stdout.fileno(), p.CHUNK_LIMIT)
                    if data:
                        if output_bytes + len(data) > p.OUTPUT_LIMIT:
                            complete = False; self.cancel.set()
                            continue
                        self.emit({'kind': 'output', 'operation_id': operation_id, 'sequence': sequence,
                                   'offset': output_bytes, 'data_b64': p.b64(data), 'sha256': p.digest(data)})
                        digest.update(data); output_bytes += len(data); sequence += 1
                    elif process.poll() is not None:
                        break
                elif process.poll() is not None:
                    # A descendant holding stdout is terminated before a receipt.
                    if self.children():
                        cancelled = True
                        method = self.terminate_children()
                    else:
                        break
                if cancelled and process.poll() is not None and not ready:
                    break
            exit_code = process.wait(timeout=1)
            process.stdout.close(); writer.join(1)
            if self.children():
                cancelled = True
                method = self.terminate_children()
            if method is None or self.children():
                self.emit({'kind': 'unknown', 'operation_id': operation_id})
                self.stop.set()
                return
            receipt = {'operation_id': operation_id, 'payload_sha256': envelope['payload_sha256'],
                       'binding_id': envelope['binding_id'], 'generation': envelope['generation'],
                       'worker_instance_id': envelope['worker_instance_id'], 'start_grant_id': grant,
                       'terminal_kind': 'cancelled' if cancelled else 'completed',
                       'exit_code': None if cancelled else exit_code, 'output_bytes': output_bytes,
                       'output_sha256': digest.hexdigest(), 'last_sequence': sequence - 1,
                       'termination_confirmed': True, 'termination_method': method,
                       'output_complete': complete, 'error_code': None if complete else 'OUTPUT_LIMIT',
                       'worker_elapsed_ms': int((time.monotonic() - started) * 1000)}
            self.emit({'kind': 'result', 'receipt': p.receipt(receipt)})
        except Exception:
            self.emit({'kind': 'unknown', 'operation_id': operation_id})
            self.stop.set()
        finally:
            if script_path:
                Path(script_path).unlink(missing_ok=True)
            self.active = None

    def main(self):
        self.emit({'kind': 'ready', 'cwd': '/workspace', 'bash': True, 'python': sys.version.split()[0]})
        control_buffer = bytearray()
        while not self.stop.is_set():
            if time.monotonic() - self.last_renewal >= 15:
                self.stop.set(); self.cancel.set()
                break
            ready, _, _ = select.select([sys.stdin.buffer], [], [], .1)
            if not ready:
                continue
            data = os.read(sys.stdin.fileno(), 65536)
            if not data:
                self.stop.set(); self.cancel.set()
                break
            control_buffer.extend(data)
            if len(control_buffer) > p.WIRE_LIMIT + 1:
                break
            while b'\n' in control_buffer:
                raw, _, remaining = control_buffer.partition(b'\n')
                control_buffer = bytearray(remaining)
                obj = p.decode(raw)
                if obj.get('action') == 'renew':
                    self.last_renewal = time.monotonic()
                elif obj.get('action') == 'cancel':
                    self.cancel.set()
                elif obj.get('action') == 'execute':
                    if self.active is not None:
                        raise RuntimeError('Container already has an operation.')
                    envelope = p.envelope(obj['envelope'])
                    grant = p.identifier(obj['start_grant_id'])
                    self.cancel.clear()
                    self.active = threading.Thread(target=self.run, args=(envelope, grant), daemon=True)
                    self.active.start()
                else:
                    raise RuntimeError('Unsupported runner action.')
        self.cancel.set()
        if self.active:
            self.active.join(4)
        self.terminate_children()


def main():
    if os.getpid() != 1:
        raise RuntimeError('Runner must be the entrypoint in its own private container PID namespace.')
    Runner().main()


if __name__ == '__main__':
    main()
