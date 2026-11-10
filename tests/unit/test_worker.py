import os
from pathlib import Path
import subprocess
import tempfile
import threading
import unittest
from unittest.mock import patch

from workbench_link.errors import Code, LinkError
from workbench_link.worker import DockerRunner, selected_project


class WorkerControlTests(unittest.TestCase):
    def runner(self):
        runner = DockerRunner.__new__(DockerRunner)
        runner.docker = 'docker'
        runner.name = 'workbench-link-test-owned'
        runner.lock = threading.Lock()
        runner.stopped = runner.stop_confirmed = False
        runner.process = subprocess.Popen(['cat'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                          stderr=subprocess.DEVNULL)
        runner.reader = threading.Thread(target=runner.process.stdout.read, daemon=True)
        runner.reader.start()
        return runner

    def test_control_close_race_does_not_escape_heartbeat_or_claim_stop(self):
        runner = self.runner()
        failures = []
        start = threading.Barrier(2)

        def renew():
            start.wait()
            for _ in range(200):
                try:
                    runner.send({'action': 'renew'})
                except LinkError as exc:
                    self.assertEqual(exc.code, Code.WORKER_UNAVAILABLE)
                    return
                except BaseException as exc:
                    failures.append(exc)
                    return
        thread = threading.Thread(target=renew)
        thread.start()
        start.wait()
        # Docker stop/inspect is unconfirmed. Repeated cleanup must retain that
        # uncertainty instead of converting an idempotent close into success.
        result = subprocess.CompletedProcess([], 1, stdout=b'', stderr=b'')
        with patch('workbench_link.worker.subprocess.run', return_value=result):
            self.assertFalse(runner.close())
            self.assertFalse(runner.close())
        thread.join(3)
        self.assertFalse(thread.is_alive())
        self.assertEqual(failures, [])
        with self.assertRaises(LinkError):
            runner.send({'action': 'renew'})

    def test_selected_project_resolves_only_explicit_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / 'project'
            project.mkdir()
            link = Path(directory) / 'selected'
            link.symlink_to(project, target_is_directory=True)
            self.assertEqual(selected_project(link), project)
            for bad in ('relative', '/', str(Path.home())):
                with self.assertRaises(LinkError):
                    selected_project(bad)
            unsupported = Path(directory) / 'bad,name'
            unsupported.mkdir()
            with self.assertRaises(LinkError):
                selected_project(unsupported)


if __name__ == '__main__':
    unittest.main()
