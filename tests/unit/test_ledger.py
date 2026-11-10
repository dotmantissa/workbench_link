import concurrent.futures
import tempfile
import unittest
from pathlib import Path

from workbench_link import protocol as p
from workbench_link.errors import Code, LinkError
from workbench_link.ledger import Ledger, new_id
from workbench_link.store import Store


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.temp.name))
        self.ledger = Ledger(self.store)
        self.instance, self.project = new_id(), new_id()
        self.image = 'sha256:' + 'a' * 64
        self.ledger.hello('dev', self.instance, self.project, 'fixture', self.image, {'bash': True})
        self.binding = self.ledger.bind(self.instance, self.project, self.image)
        self.env = self.ledger.open_environment()

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def envelope(self):
        obj = {'protocol_version': 1, 'profile_id': self.env['profile_id'],
               'binding_id': self.env['binding_id'], 'generation': self.env['generation'],
               'environment_id': self.env['environment_id'], 'operation_id': new_id(),
               'worker_id': 'dev', 'worker_instance_id': self.instance, 'project_id': self.project,
               'script': 'printf fixture', 'stdin_b64': '', 'login': False, 'timeout_seconds': 10}
        obj['payload_sha256'] = p.payload_hash(obj)
        return obj

    def grant(self, e):
        self.ledger.submit(e)
        return self.ledger.accept(self.instance, e['operation_id'], e['payload_sha256'])['start_grant_id']

    def receipt(self, e, grant, output=b'', **changes):
        obj = {'operation_id': e['operation_id'], 'payload_sha256': e['payload_sha256'],
               'binding_id': e['binding_id'], 'generation': e['generation'],
               'worker_instance_id': self.instance, 'start_grant_id': grant,
               'terminal_kind': 'completed', 'exit_code': 1,
               'output_bytes': len(output), 'output_sha256': p.digest(output),
               'last_sequence': (len(output) + p.CHUNK_LIMIT - 1) // p.CHUNK_LIMIT - 1,
               'termination_confirmed': True, 'termination_method': 'natural',
               'output_complete': True, 'error_code': None, 'worker_elapsed_ms': 10}
        obj.update(changes)
        return obj

    def upload(self, e, output):
        for sequence, offset in enumerate(range(0, len(output), p.CHUNK_LIMIT)):
            data = output[offset:offset + p.CHUNK_LIMIT]
            self.ledger.output(self.instance, e['operation_id'], sequence, offset, data, p.digest(data))

    def test_grant_and_output_duplicates_have_one_identity(self):
        e = self.envelope()
        grant = self.grant(e)
        self.assertEqual(self.ledger.accept(self.instance, e['operation_id'], e['payload_sha256'])['start_grant_id'], grant)
        self.assertEqual(self.ledger.submit(e)['state'], 'START_GRANTED')
        output = b'\x00\xff\r\nno newline' * 7000
        self.upload(e, output)
        self.upload(e, output)
        receipt = self.receipt(e, grant, output)
        self.assertTrue(self.ledger.result(self.instance, receipt)['acknowledged'])
        self.assertTrue(self.ledger.result(self.instance, receipt)['acknowledged'])
        self.assertEqual(self.ledger.read_output(e['operation_id'], maximum=p.OUTPUT_LIMIT), output)
        self.assertEqual(self.ledger.operation(e['operation_id'])['receipt']['exit_code'], 1)
        self.assertEqual(self.ledger.operation(e['operation_id'])['state'], 'COMPLETED')

    def test_payload_conflict_fence_survives_restart(self):
        e = self.envelope()
        self.ledger.submit(e)
        changed = dict(e, script='different effect')
        changed['payload_sha256'] = p.payload_hash(changed)
        with self.assertRaises(LinkError) as caught:
            self.ledger.submit(changed)
        self.assertEqual(caught.exception.code, Code.PAYLOAD_CONFLICT)
        self.store.close()
        self.store = Store(Path(self.temp.name)); self.ledger = Ledger(self.store)
        self.ledger.recover_startup()
        self.assertEqual(self.ledger.status()['binding']['state'], 'FENCED')
        with self.assertRaises(LinkError) as caught:
            self.ledger.open_environment()
        self.assertEqual(caught.exception.code, Code.OUTCOME_UNKNOWN)

    def test_cancel_grant_race_never_claims_no_start_after_grant(self):
        for _ in range(20):
            # A distinct isolated binding per race; no implicit fence clearing.
            with tempfile.TemporaryDirectory() as directory:
                store = Store(Path(directory)); ledger = Ledger(store)
                instance, project = new_id(), new_id()
                ledger.hello('dev', instance, project, 'fixture', self.image, {})
                ledger.bind(instance, project, self.image)
                env = ledger.open_environment()
                e = self.envelope()
                for name in ('profile_id', 'binding_id', 'generation', 'environment_id'):
                    e[name] = env[name]
                e.update(worker_instance_id=instance, project_id=project)
                e['payload_sha256'] = p.payload_hash(e)
                ledger.submit(e)
                with concurrent.futures.ThreadPoolExecutor(2) as pool:
                    futures = [pool.submit(ledger.cancel, e['operation_id']),
                               pool.submit(ledger.accept, instance, e['operation_id'], e['payload_sha256'])]
                    for future in futures:
                        try:
                            future.result()
                        except LinkError:
                            pass
                row = ledger._op(e['operation_id'])
                if row['grant_id']:
                    self.assertNotEqual(row['state'], 'NOT_STARTED')
                    self.assertEqual(ledger.status()['binding']['state'], 'FENCED')
                else:
                    self.assertEqual(row['state'], 'NOT_STARTED')
                store.close()

    def test_restart_and_late_receipt_do_not_relaunch_or_clear_fence(self):
        e = self.envelope(); grant = self.grant(e)
        self.store.close()
        self.store = Store(Path(self.temp.name)); self.ledger = Ledger(self.store)
        self.ledger.recover_startup()
        self.assertEqual(self.ledger.operation(e['operation_id'])['state'], 'UNKNOWN')
        with self.assertRaises(LinkError):
            self.ledger.accept(self.instance, e['operation_id'], e['payload_sha256'])
        self.ledger.result(self.instance, self.receipt(e, grant))
        self.assertEqual(self.ledger.operation(e['operation_id'])['state'], 'COMPLETED')
        self.assertEqual(self.ledger.status()['binding']['state'], 'FENCED')

    def test_missing_output_fails_without_regeneration(self):
        e = self.envelope(); grant = self.grant(e)
        self.upload(e, b'effect')
        (self.store.spool / p.digest(b'effect')).unlink()
        with self.assertRaises(LinkError) as caught:
            self.ledger.result(self.instance, self.receipt(e, grant, b'effect'))
        self.assertEqual(caught.exception.code, Code.INTEGRITY_FAILURE)
        self.assertNotEqual(self.ledger.operation(e['operation_id'])['state'], 'COMPLETED')
        self.assertEqual(self.ledger.status()['binding']['state'], 'FENCED')

    def test_conflicting_output_and_receipts_fence(self):
        e = self.envelope(); grant = self.grant(e)
        self.upload(e, b'x')
        with self.assertRaises(LinkError):
            self.ledger.output(self.instance, e['operation_id'], 0, 0, b'y', p.digest(b'y'))
        self.assertEqual(self.ledger.status()['binding']['state'], 'FENCED')
        receipt = self.receipt(e, grant, b'x')
        self.ledger.result(self.instance, receipt)
        with self.assertRaises(LinkError):
            self.ledger.result(self.instance, dict(receipt, exit_code=0))
        self.assertEqual(self.ledger.operation(e['operation_id'])['receipt']['exit_code'], 1)

    def test_identity_and_single_environment_are_enforced(self):
        with self.assertRaises(LinkError) as caught:
            self.ledger.open_environment()
        self.assertEqual(caught.exception.code, Code.WORKSPACE_BUSY)
        e = self.envelope()
        e['profile_id'] = new_id(); e['payload_sha256'] = p.payload_hash(e)
        with self.assertRaises(LinkError):
            self.ledger.submit(e)
        self.assertEqual(len(self.ledger.status()['operations']), 0)

    def test_gap_and_false_success_receipts_are_refused(self):
        e = self.envelope(); grant = self.grant(e)
        with self.assertRaises(LinkError):
            self.ledger.output(self.instance, e['operation_id'], 1, 0, b'x', p.digest(b'x'))
        with self.assertRaises(LinkError):
            self.ledger.result(self.instance, self.receipt(e, grant, b'x'))
        self.assertEqual(self.ledger.operation(e['operation_id'])['state'], 'START_GRANTED')


if __name__ == '__main__':
    unittest.main()
