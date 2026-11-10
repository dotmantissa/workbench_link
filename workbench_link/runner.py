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

    def inventory(self):
        processes = []
        for pid in self.children():
            try:
                raw = Path(f'/proc/{pid}/stat').read_text()
                fields = raw[raw.rindex(')') + 2:].split()
                if fields[0] != 'Z':
                    processes.append({'pid': pid, 'start_ticks': int(fields[19])})
            except FileNotFoundError:
                continue
        return p.process_inventory(processes)

    def reap(self):
        try:
            while os.waitpid(-1, os.WNOHANG)[0]:
                pass
        except ChildProcessError:
            pass

    def terminate_tree(self, target):
        inventory = self.inventory()
        if target not in inventory:
            return 1
        group = os.getpgid(target['pid'])
        if group <= 1:
            raise RuntimeError('Refusing runner process group termination.')
        selected = [target]
        parents = {}
        for process in inventory:
            try:
                raw = Path(f"/proc/{process['pid']}/stat").read_text()
                parents[process['pid']] = int(raw[raw.rindex(')') + 2:].split()[1])
            except FileNotFoundError:
                continue
        while True:
            descendants = [process for process in inventory if process not in selected and
                           parents.get(process['pid']) in {item['pid'] for item in selected}]
            if not descendants:
                break
            selected.extend(descendants)
        for signum, grace in ((signal.SIGTERM, 2), (signal.SIGKILL, 1)):
            if signum == signal.SIGKILL:
                # A TERM-ignoring supervisor may spawn another child during its
                # grace window. Its private launch group keeps those orphans owned.
                for process in self.inventory():
                    try:
                        if os.getpgid(process['pid']) == group and process not in selected:
                            selected.append(process)
                    except ProcessLookupError:
                        continue
                try:
                    os.killpg(group, signum)
                except ProcessLookupError:
                    pass
            # Parent first; then snapshot survivors, always matching start time.
            for index, process in enumerate(selected):
                if process in self.inventory():
                    try:
                        os.kill(process['pid'], signum)
                    except ProcessLookupError:
                        pass
                if index == 0:
                    time.sleep(.1)
            deadline = time.monotonic() + grace
            while time.monotonic() < deadline:
                self.reap()
                live = self.inventory()
                for process in live:
                    try:
                        if os.getpgid(process['pid']) == group and process not in selected:
                            selected.append(process)
                    except ProcessLookupError:
                        continue
                if not any(process in live for process in selected):
                    return 0
                time.sleep(.02)
        raise RuntimeError('Process tree termination remains unknown.')

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
        session = envelope.get('lifecycle') == 'session'
        exited_at = None
        try:
            signal_result = self.terminate_tree(envelope['terminate_process']) if 'terminate_process' in envelope else None
            fd, script_path = tempfile.mkstemp(prefix='workbench-script-', dir='/tmp')
            with os.fdopen(fd, 'wb') as script:
                script.write((f'exit {signal_result}' if signal_result is not None else envelope['script']).encode('utf-8'))
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
                if session and not cancelled and process.poll() is not None:
                    exited_at = exited_at or time.monotonic()
                    # Native background wrappers retain the pipe but redirect the
                    # job's output to a separate log. Foreground capture ends here.
                    if not ready:
                        break
                    if time.monotonic() - exited_at > .5:
                        # Continuous inherited-pipe output cannot be attributed
                        # to the exited foreground shell. Never call a bounded
                        # cutoff complete: stop the environment and reject data.
                        complete = False
                        cancelled = True
                        method = self.terminate_children()
                        break
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
                    if self.children() and not session:
                        cancelled = True
                        method = self.terminate_children()
                    else:
                        break
                if cancelled and process.poll() is not None and not ready:
                    break
            exit_code = process.wait(timeout=1)
            process.stdout.close(); writer.join(1)
            if self.children() and (cancelled or not session):
                cancelled = True
                method = self.terminate_children()
            self.reap()
            detached = self.inventory() if session and not cancelled else []
            if method is None or ((cancelled or not session) and self.children()):
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
            if session:
                receipt.update(termination_scope='environment' if cancelled else 'foreground',
                               detached_processes=detached)
            # All cleanup and inventory are complete before the worker can send
            # another command after receiving this receipt.
            self.active = None
            self.emit({'kind': 'result', 'receipt': p.receipt(receipt)})
        except Exception:
            self.emit({'kind': 'unknown', 'operation_id': operation_id})
            self.stop.set()
        finally:
            if script_path:
                Path(script_path).unlink(missing_ok=True)
            if self.active is threading.current_thread():
                self.active = None

    def main(self):
        self.emit({'kind': 'ready', 'cwd': '/workspace', 'bash': True, 'python': sys.version.split()[0],
                   'protocol_version': p.VERSION, 'session_lifecycle': 1})
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
