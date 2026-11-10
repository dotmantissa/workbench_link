"""Native management commands. The foreground broker starts only by explicit CLI."""

import json
import signal
import ssl
import sys
import time

from . import control
from .errors import Code, LinkError
from .settings import key_bytes


def setup_parser(parser):
    commands = parser.add_subparsers(dest='link_command', required=True)
    for name in ('status', 'doctor', 'operations', 'recover', 'stop', 'reset'):
        sub = commands.add_parser(name, help='Inspect this profile and its selected worker')
        sub.add_argument('--json', action='store_true')
    for name in ('inspect', 'cancel', 'resolve'):
        sub = commands.add_parser(name, help='Inspect, cancel or record human resolution of an operation')
        sub.add_argument('operation_id')
        sub.add_argument('--json', action='store_true')
        if name == 'inspect':
            sub.add_argument('--output', action='store_true', help='Write exact retained output bytes to stdout')
        if name == 'resolve':
            sub.add_argument('--note', required=True, help='Local inspection findings; do not include secrets')
    bind = commands.add_parser('bind', help='Accept exact worker instance, project and image identities')
    bind.add_argument('--instance-id', required=True)
    bind.add_argument('--project-id', required=True)
    bind.add_argument('--image', required=True)
    bind.add_argument('--json', action='store_true')
    serve = commands.add_parser('serve', help='Run this profile broker in the foreground')
    serve.add_argument('--listen', default='127.0.0.1')
    serve.add_argument('--port', type=int, default=8765)
    serve.add_argument('--local-test', action='store_true', help='Allow plain HTTP on literal loopback for local tests')
    serve.add_argument('--tls-cert')
    serve.add_argument('--tls-key')


def emit(result, json_mode=False):
    if json_mode:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return
    if result.get('ok') is False:
        print(f"{result['code']}: {result['message']}")
        return
    if 'operation_id' in result:
        print(f"Operation: {result['operation_id']} · {result['state']}")
        print(f"Cancellation requested: {result['cancel_requested']} · retained output: {result['output_bytes']} bytes")
        if result['receipt']:
            receipt = result['receipt']
            print(f"Receipt: {receipt['terminal_kind']} · exit {receipt['exit_code']} · termination {receipt.get('termination_scope', 'environment')}")
        return
    binding = result.get('binding')
    print(f"Profile: {result.get('profile_id', 'accepted')}")
    if binding:
        print(f"Project: {binding['alias']} · worker {binding['worker_id']} · generation {binding['generation']}")
        print(f"State: {binding['state']} · connected: {result.get('connected', False)}")
        print(f"Image: {binding['image']}")
    else:
        print('No accepted project. Start a worker, inspect status --json, then bind its exact identities.')
    for registration in result.get('registrations', []):
        print(f"Worker: {registration['worker_id']} · instance {registration['instance_id']} · project {registration['project_id']}")
    for environment in result.get('environments', []):
        print(f"Environment: {environment['environment_id']} · {environment['state']} · stop confirmed: {bool(environment['stop_evidence'])}")
    for operation in result.get('operations', []):
        print(f"Operation: {operation['operation_id']} · {operation['state']}")


def run_cli(args, settings, secret):
    broker = None
    previous = {}
    try:
        if args.link_command == 'serve':
            from .broker import Broker
            context = None
            if bool(args.tls_cert) != bool(args.tls_key):
                raise ValueError('Supply both --tls-cert and --tls-key.')
            if args.tls_cert:
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                context.minimum_version = ssl.TLSVersion.TLSv1_2
                context.load_cert_chain(args.tls_cert, args.tls_key)
            broker = Broker(settings, key_bytes(secret), (args.listen, args.port),
                            local_test=args.local_test, tls_context=context).start()
            for signum in (signal.SIGINT, signal.SIGTERM):
                previous[signum] = signal.signal(signum, lambda *_: broker.stop_event.set())
            print(f'Broker listening on {args.listen}:{broker.http.server_address[1]}; private control {settings.control_dir}', flush=True)
            while not broker.stop_event.wait(.5):
                pass
            return 0
        if args.link_command == 'bind':
            result = control.request(settings.control_dir, 'bind', instance_id=args.instance_id,
                                     project_id=args.project_id, image=args.image)
            emit(control.request(settings.control_dir, 'status'), args.json)
            return 0
        if args.link_command in ('inspect', 'cancel', 'resolve'):
            if args.link_command == 'resolve':
                if not sys.stdin.isatty() or not sys.stdout.isatty():
                    raise LinkError(Code.BAD_REQUEST, 'Unknown resolution requires an interactive human terminal.')
                current = control.request(settings.control_dir, 'operation_status', operation_id=args.operation_id)
                emit(current)
                print('Effects remain unknown. Confirm that you inspected the project locally. History is retained; no command will replay.')
                confirmation = input('Type the complete operation ID to record your resolution: ').strip()
                result = control.request(settings.control_dir, 'resolve_unknown', operation_id=args.operation_id,
                    note=args.note, confirmation=confirmation)
            else:
                result = control.request(settings.control_dir, 'cancel' if args.link_command == 'cancel' else 'operation_status',
                                         operation_id=args.operation_id)
            if getattr(args, 'output', False):
                from . import protocol as p
                if args.json:
                    raise LinkError(Code.BAD_REQUEST, 'Choose --output or --json.')
                offset = 0
                while offset < result['output_bytes']:
                    data = p.unb64(control.request(settings.control_dir, 'read_output',
                        operation_id=args.operation_id, offset=offset)['data_b64'], p.CHUNK_LIMIT)
                    if not data:
                        raise LinkError(Code.INTEGRITY_FAILURE, 'Retained output has a gap.', args.operation_id)
                    sys.stdout.buffer.write(data)
                    offset += len(data)
            else:
                emit(result, args.json)
            return 3 if result['state'] in ('UNKNOWN', 'START_GRANTED', 'RUNNING') and args.link_command != 'inspect' else 0
        if args.link_command in ('recover', 'stop', 'reset'):
            result = control.request(settings.control_dir, args.link_command)
            deadline = time.monotonic() + (8 if args.link_command == 'stop' else 2)
            while time.monotonic() < deadline:
                pending = result['unresolved_count'] > 0
                closing = result['closing_count'] > 0
                if not pending and not closing:
                    break
                time.sleep(.1)
                result = control.request(settings.control_dir, 'status')
            emit(result, args.json)
            return 3 if pending or closing else 0
        result = control.request(settings.control_dir, 'status')
        if args.link_command == 'doctor':
            result['checks'] = {'private_ipc': True, 'connected': result['connected'],
                'active_binding': bool(result['binding'] and result['binding']['state'] == 'ACTIVE'),
                'configured_worker': bool(result['binding'] and result['binding']['worker_id'] == settings.worker_id)}
        emit(result, args.json)
        return 0 if result['connected'] and result['binding']['state'] == 'ACTIVE' else 3
    except LinkError as exc:
        emit(exc.as_dict(), getattr(args, 'json', False))
        return 2 if exc.code in ('BAD_REQUEST', 'AUTH_FAILED') else 3
    except (ValueError, OSError) as exc:
        print(f'Setup failed: {type(exc).__name__}. Check listener and certificate settings.')
        return 2
    finally:
        if broker:
            broker.close()
        for signum, handler in previous.items():
            signal.signal(signum, handler)
