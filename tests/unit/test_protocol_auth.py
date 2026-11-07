import copy
import tempfile
import unittest
import uuid
from pathlib import Path

from workbench_link import auth, protocol as p
from workbench_link.errors import Code, LinkError
from workbench_link.settings import broker_url, key_bytes
from workbench_link.store import Store


def envelope(**changes):
    obj = {name: str(uuid.uuid4()) for name in
           ('profile_id', 'binding_id', 'environment_id', 'operation_id', 'worker_instance_id', 'project_id')}
    obj.update(protocol_version=1, generation=1, worker_id='local-dev', script='printf λ', login=False,
               stdin_b64=p.b64('字\r\nno newline'.encode()), timeout_seconds=120)
    obj.update(changes)
    obj['payload_sha256'] = p.payload_hash(obj)
    return obj


class ProtocolTests(unittest.TestCase):
    def test_exact_bytes_roundtrip(self):
        e = envelope()
        self.assertEqual(p.envelope(p.decode(p.canonical(e))), e)
        self.assertEqual(p.unb64(e['stdin_b64'], p.STDIN_LIMIT), '字\r\nno newline'.encode())

    def test_reject_ambiguous_inputs(self):
        for raw in (b'{"a":1,"a":2}', b'{"x":NaN}', b'[]', b'\xff'):
            with self.subTest(raw=raw), self.assertRaises(LinkError):
                p.decode(raw)
        for changes in ({'timeout_seconds': True}, {'generation': 0}, {'login': 1}, {'worker_id': '../x'},
                        {'stdin_b64': 'AB=='}, {'extra': 1}, {'script': '\x00'}):
            with self.subTest(changes=changes), self.assertRaises(LinkError):
                p.envelope(envelope(**changes))

    def test_tampering_and_bounds(self):
        e = envelope(); e['script'] += 'changed'
        with self.assertRaises(LinkError) as caught:
            p.envelope(e)
        self.assertEqual(caught.exception.code, Code.PAYLOAD_CONFLICT)
        with self.assertRaises(LinkError):
            p.unb64('A' * 100, 4)
        with self.assertRaises(LinkError):
            p.envelope(envelope(script='λ' * (p.SCRIPT_LIMIT // 2 + 1)))

    def test_url_auth_rules(self):
        self.assertEqual(broker_url('http://127.0.0.1:8765/', True), 'http://127.0.0.1:8765')
        for url, local in [('http://example.org', True), ('http://localhost', False),
                           ('https://user:secret@example.org', False), ('https://example.org?q=1', False)]:
            with self.subTest(url=url), self.assertRaises(LinkError):
                broker_url(url, local)
        self.assertEqual(key_bytes('ab' * 32), b'\xab' * 32)
        with self.assertRaises(LinkError) as caught:
            key_bytes('sensitive-invalid-value')
        self.assertNotIn('sensitive-invalid-value', str(caught.exception))


class AuthTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.temp.name))
        self.key = b'x' * 32
        self.instance = str(uuid.uuid4())
        self.body = p.canonical({'protocol_version': 1})
        self.path = '/v1/worker/hello'

    def tearDown(self):
        self.store.close(); self.temp.cleanup()

    def test_signed_request_replay_and_new_nonce_retry(self):
        headers = auth.sign(self.key, self.path, 'dev', self.instance, self.body, now=100)
        args = (self.key, 'dev', 'POST', self.path, headers, self.body, self.store.consume_nonce)
        self.assertEqual(auth.verify(*args, now=100), ('dev', self.instance))
        with self.assertRaises(LinkError):
            auth.verify(*args, now=100)
        other = auth.sign(self.key, self.path, 'dev', self.instance, self.body, now=100)
        auth.verify(self.key, 'dev', 'POST', self.path, other, self.body, self.store.consume_nonce, now=100)

    def test_tampering_before_nonce_mutation(self):
        headers = auth.sign(self.key, self.path, 'dev', self.instance, self.body, now=100)
        for name, value in [('X-WBL-Worker', 'other'), ('X-WBL-Time', '0'), ('X-WBL-Version', '2'),
                            ('X-WBL-Signature', '0' * 64), ('X-WBL-Instance', 'invalid')]:
            changed = copy.copy(headers); changed[name] = value
            with self.subTest(name=name), self.assertRaises(LinkError):
                auth.verify(self.key, 'dev', 'POST', self.path, changed, self.body, self.store.consume_nonce, now=100)
        for path in (self.path + '?x=1', '/v1/operator/submit'):
            with self.assertRaises(LinkError):
                auth.verify(self.key, 'dev', 'POST', path, headers, self.body, self.store.consume_nonce, now=100)
        with self.assertRaises(LinkError):
            auth.verify(self.key, 'dev', 'POST', self.path, headers, b'changed', self.store.consume_nonce, now=100)
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM nonces').fetchone()[0], 0)

    def test_nonce_survives_restart(self):
        self.assertTrue(self.store.consume_nonce('dev', 'nonce', 100))
        profile = self.store.profile_id
        self.store.close(); self.store = Store(Path(self.temp.name))
        self.assertEqual(self.store.profile_id, profile)
        self.assertFalse(self.store.consume_nonce('dev', 'nonce', 101))
        self.assertTrue(self.store.consume_nonce('dev', 'nonce', 221))

    def test_spool_missing_never_regenerates(self):
        ref = self.store.publish(b'output\r\nno newline')
        self.assertEqual(self.store.read(ref), b'output\r\nno newline')
        (self.store.spool / ref).unlink()
        with self.assertRaises(LinkError) as caught:
            self.store.read(ref)
        self.assertEqual(caught.exception.code, Code.INTEGRITY_FAILURE)

    def test_transaction_rollback(self):
        with self.assertRaises(RuntimeError):
            with self.store.transaction():
                self.store.put('test', '1', {'value': 1})
                raise RuntimeError('crash')
        self.assertIsNone(self.store.get('test', '1'))


if __name__ == '__main__':
    unittest.main()
