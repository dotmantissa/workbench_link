"""Native management commands. The foreground broker starts only by explicit CLI."""

import json
import signal
import ssl

from . import control
from .errors import LinkError
from .settings import key_bytes


def setup_parser(parser):
    commands = parser.add_subparsers(dest='link_command', required=True)
    for name in ('status', 'doctor'):
        sub = commands.add_parser(name, help='Inspect this profile and its selected worker')
        sub.add_argument('--json', action='store_true')
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
            emit(result, args.json)
            return 0
        result = control.request(settings.control_dir, 'status')
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
