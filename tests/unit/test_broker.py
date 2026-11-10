import http.client
import os
import socket
import struct
import tempfile
import time
import unittest
from pathlib import Path

from workbench_link import auth, control, protocol as p
from workbench_link.broker import Broker
from workbench_link.errors import Code, LinkError
from workbench_link.ledger import new_id
from workbench_link.settings import Settings
from workbench_link.transport import WorkerClient


class BrokerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.settings = Settings('dev', 'fixture', self.root)
        self.key = b'x' * 32
        self.broker = Broker(self.settings, self.key, ('127.0.0.1', 0), local_test=True).start()
        self.port = self.broker.http.server_address[1]
        self.instance, self.project = new_id(), new_id()
        self.image = 'sha256:' + 'a' * 64
        self.client = WorkerClient(f'http://127.0.0.1:{self.port}', 'dev', self.instance, self.key, local_test=True)

    def tearDown(self):
        self.broker.close(); self.temp.cleanup()

    def hello_bind(self):
        self.client.post('hello', {'protocol_version': 1, 'project_id': self.project,
                                 'alias': 'fixture', 'image': self.image, 'capabilities': {}})
        control.request(self.root, 'bind', instance_id=self.instance, project_id=self.project, image=self.image)

    def test_private_control_permissions_and_single_owner(self):
        self.assertEqual(os.stat(self.root / 'control.sock').st_mode & 0o777, 0o600)
        self.assertTrue(control.request(self.root, 'status')['ok'])
        with self.assertRaises(LinkError) as caught:
            Broker(self.settings, self.key, ('127.0.0.1', 0), local_test=True)
        self.assertEqual(caught.exception.code, Code.WORKSPACE_BUSY)
        self.assertTrue(control.request(self.root, 'status')['ok'])

    def test_worker_cannot_submit_or_bind_and_wrong_key_cannot_register(self):
        body = p.canonical({'action': 'submit'})
        for path in ('/v1/worker/submit', '/v1/operator/bind'):
            connection = http.client.HTTPConnection('127.0.0.1', self.port, timeout=3)
            connection.request('POST', path, body, auth.sign(self.key, path, 'dev', self.instance, body))
            result = connection.getresponse()
            self.assertEqual(result.status, 400); result.read(); connection.close()
        wrong = WorkerClient(f'http://127.0.0.1:{self.port}', 'dev', self.instance, b'y' * 32, local_test=True)
        with self.assertRaises(LinkError) as caught:
            wrong.post('hello', {})
        self.assertEqual(caught.exception.code, Code.AUTH_FAILED)
        self.assertEqual(control.request(self.root, 'status')['registrations'], [])

    def test_live_worker_required_and_generation_lease_checked(self):
        with self.assertRaises(LinkError):
            control.request(self.root, 'open_environment')
        self.hello_bind()
        identity = control.request(self.root, 'open_environment')
        heartbeat = {'binding_id': identity['binding_id'], 'generation': identity['generation'], 'active_operation_id': None}
        self.assertTrue(self.client.post('heartbeat', heartbeat)['ok'])
        with self.assertRaises(LinkError) as caught:
            self.client.post('heartbeat', dict(heartbeat, generation=2))
        self.assertEqual(caught.exception.code, Code.BINDING_STALE)
        with self.broker.heartbeat_lock:
            self.broker.heartbeats[self.instance] = time.monotonic() - 16
        self.assertFalse(control.request(self.root, 'status')['connected'])

    def test_oversized_frames_and_duplicate_headers_refused(self):
        connection = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        connection.connect(str(self.root / 'control.sock'))
        connection.sendall(struct.pack('!I', p.CONTROL_LIMIT + 1))
        result = control.receive(connection, time.monotonic() + 2)
        self.assertEqual(result['code'], 'BAD_REQUEST'); connection.close()
        connection = http.client.HTTPConnection('127.0.0.1', self.port, timeout=3)
        connection.putrequest('POST', '/v1/worker/hello')
        connection.putheader('Content-Length', '2'); connection.putheader('Content-Length', '2')
        connection.endheaders(b'{}')
        response = connection.getresponse()
        self.assertEqual(response.status, 400); response.read(); connection.close()

    def test_stale_socket_recovery_preserves_identity(self):
        identity = control.request(self.root, 'status')['profile_id']
        self.broker.close()
        stale = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        stale.bind(str(self.root / 'control.sock')); stale.close()
        self.broker = Broker(self.settings, self.key, ('127.0.0.1', 0), local_test=True).start()
        self.assertEqual(control.request(self.root, 'status')['profile_id'], identity)


if __name__ == '__main__':
    unittest.main()
