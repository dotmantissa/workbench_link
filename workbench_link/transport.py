"""Worker requests: fresh nonces, verified TLS, bounded bodies, no redirects."""

import http.client
import ssl
import socket
import threading
from urllib.parse import urlsplit

from . import auth, protocol as p
from .errors import Code, LinkError
from .settings import broker_url


class WorkerClient:
    def __init__(self, url, worker_id, instance_id, key, *, local_test=False, ca_file=None):
        self.url = urlsplit(broker_url(url, local_test))
        self.worker_id, self.instance_id, self.key = worker_id, instance_id, key
        self.context = ssl.create_default_context(cafile=ca_file)

    def post(self, action, obj):
        path = '/v1/worker/' + action
        if path not in auth.PATHS:
            p.bad('Unsupported worker request.')
        body = p.canonical(obj)
        if len(body) > p.WIRE_LIMIT:
            p.bad('Worker request exceeds the wire limit.')
        headers = auth.sign(self.key, path, self.worker_id, self.instance_id, body)
        headers['Content-Type'] = 'application/json'
        constructor = http.client.HTTPSConnection if self.url.scheme == 'https' else http.client.HTTPConnection
        options = {'context': self.context} if self.url.scheme == 'https' else {}
        connection = constructor(self.url.hostname, self.url.port, timeout=3, **options)
        expired = threading.Event()

        def abort():
            expired.set()
            sock = connection.sock
            if sock:
                try:
                    sock.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
            connection.close()
        timer = threading.Timer(3, abort)
        timer.daemon = True
        timer.start()
        try:
            # http.client uses no environment proxy settings or redirect machinery.
            connection.request('POST', path, body, headers)
            response = connection.getresponse()
            if 300 <= response.status < 400:
                raise LinkError(Code.AUTH_FAILED, 'Broker redirects are refused.')
            raw = response.read(p.WIRE_LIMIT + 1)
            if expired.is_set():
                raise LinkError(Code.WORKER_UNAVAILABLE, 'Broker response deadline exceeded; reconcile without replay.')
            result = p.decode(raw)
        except ssl.SSLCertVerificationError:
            raise LinkError(Code.AUTH_FAILED, 'Broker TLS identity could not be verified. Check hostname and trusted CA.') from None
        except (OSError, http.client.HTTPException):
            raise LinkError(Code.WORKER_UNAVAILABLE, 'Broker transport is unavailable; reconcile using the same operation IDs.') from None
        finally:
            timer.cancel()
            connection.close()
        if response.status != 200 or result.get('ok') is not True:
            try:
                code = Code(result['code'])
            except (ValueError, KeyError):
                code = Code.INTEGRITY_FAILURE
            raise LinkError(code, result.get('message', 'Invalid broker response.'), result.get('operation_id'))
        return result
