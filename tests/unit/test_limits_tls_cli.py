import argparse
import contextlib
import io
import os
from pathlib import Path
import socket
import ssl
import subprocess
import tempfile
import time
import unittest
from unittest.mock import patch

from workbench_link.broker import Broker
from workbench_link.cli import run_cli, setup_parser
from workbench_link.errors import Code, LinkError
from workbench_link.ledger import new_id
from workbench_link.settings import Settings
from workbench_link.store import Store
from workbench_link.transport import WorkerClient


class LimitsTests(unittest.TestCase):
    def test_quota_and_disk_failure_never_acknowledge_unpublished_data(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Store(Path(directory))
            try:
                with patch('workbench_link.store.SPOOL_LIMIT', 4):
                    ref = store.publish(b'abcd')
                    self.assertEqual(store.publish(b'abcd'), ref)
                    with self.assertRaises(LinkError) as caught:
                        store.publish(b'e')
                    self.assertEqual(caught.exception.code, Code.OUTPUT_LIMIT)
                with patch('workbench_link.store.os.fsync', side_effect=OSError('disk failure')):
                    with self.assertRaises(LinkError) as caught:
                        store.publish(b'new output')
                    self.assertEqual(caught.exception.code, Code.STORAGE_UNAVAILABLE)
                self.assertEqual([path.name for path in store.spool.iterdir()], [ref])
                self.assertEqual(store.read(ref), b'abcd')
            finally:
                store.close()

    def test_schema_one_migrates_without_losing_identity_and_unknown_versions_refuse(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Store(Path(directory)); identity = store.profile_id
            store.db.execute('PRAGMA user_version=1'); store.close()
            store = Store(Path(directory))
            self.assertEqual(store.profile_id, identity)
            self.assertEqual(store.db.execute('PRAGMA user_version').fetchone()[0], 2)
            store.db.execute('PRAGMA user_version=999'); store.close()
            with self.assertRaises(LinkError):
                Store(Path(directory))

    def test_cli_refuses_noninteractive_unknown_resolution(self):
        parser = argparse.ArgumentParser(); setup_parser(parser)
        args = parser.parse_args(['resolve', new_id(), '--note', 'Checked project'])
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()) as output:
            code = run_cli(args, Settings('dev', 'fixture', Path(directory)), '')
        self.assertEqual(code, 2)
        self.assertIn('interactive human terminal', output.getvalue())

    def test_work_capacity_keeps_heartbeat_available(self):
        with tempfile.TemporaryDirectory() as directory:
            settings = Settings('dev', 'fixture', Path(directory))
            key = os.urandom(32)
            broker = Broker(settings, key, ('127.0.0.1', 0), local_test=True).start()
            try:
                client = WorkerClient(f'http://127.0.0.1:{broker.http.server_port}', 'dev', new_id(), key, local_test=True)
                for _ in range(12):
                    self.assertTrue(broker.http.work_capacity.acquire(blocking=False))
                heartbeat = client.post('heartbeat', {'binding_id': None, 'generation': None, 'active_operation_id': None})
                self.assertTrue(heartbeat['ok'])
                with self.assertRaises(LinkError) as caught:
                    client.post('poll', {})
                self.assertEqual(caught.exception.code, Code.WORKSPACE_BUSY)
            finally:
                broker.close()


class TLSTests(unittest.TestCase):
    def test_verified_tls_rejects_untrusted_host_and_stalled_handshake_does_not_block_accept(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cert, keyfile = root / 'cert.pem', root / 'key.pem'
            subprocess.run(['openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-nodes',
                '-keyout', str(keyfile), '-out', str(cert), '-days', '1', '-subj', '/CN=localhost',
                '-addext', 'subjectAltName=DNS:localhost'], check=True, capture_output=True, timeout=10)
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(cert, keyfile)
            shared = os.urandom(32)
            broker = Broker(Settings('dev', 'fixture', root / 'state'), shared,
                            ('127.0.0.1', 0), tls_context=context).start()
            slow = socket.create_connection(broker.http.server_address, timeout=3)
            try:
                port = broker.http.server_port
                client = WorkerClient(f'https://localhost:{port}', 'dev', new_id(), shared, ca_file=str(cert))
                started = time.monotonic()
                client.post('heartbeat', {'binding_id': None, 'generation': None, 'active_operation_id': None})
                self.assertLess(time.monotonic() - started, 2)
                for url, ca in ((f'https://localhost:{port}', None), (f'https://127.0.0.1:{port}', str(cert))):
                    with self.assertRaises(LinkError) as caught:
                        WorkerClient(url, 'dev', new_id(), shared, ca_file=ca).post('poll', {})
                    self.assertEqual(caught.exception.code, Code.AUTH_FAILED)
            finally:
                slow.close(); broker.close()


if __name__ == '__main__':
    unittest.main()
