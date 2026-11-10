"""Bounded private control framing; no TCP fallback or implicit service startup."""

import os
import socket
import struct
import time
from pathlib import Path

from . import protocol as p
from .errors import Code, LinkError


def receive_exact(sock, count, deadline):
    data = bytearray()
    while len(data) < count:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError('Control deadline exceeded.')
        sock.settimeout(remaining)
        part = sock.recv(min(65536, count - len(data)))
        if not part:
            raise ConnectionError('Control connection closed.')
        data.extend(part)
    return bytes(data)


def receive(sock, deadline):
    size = struct.unpack('!I', receive_exact(sock, 4, deadline))[0]
    if not 1 <= size <= p.CONTROL_LIMIT:
        p.bad('Control frame exceeds the limit.')
    return p.decode(receive_exact(sock, size, deadline), p.CONTROL_LIMIT)


def send(sock, value, deadline):
    data = p.canonical(value)
    if len(data) > p.CONTROL_LIMIT:
        p.bad('Control response exceeds the limit.')
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise TimeoutError('Control deadline exceeded.')
    sock.settimeout(remaining)
    sock.sendall(struct.pack('!I', len(data)) + data)


def check_peer(sock):
    _, uid, _ = struct.unpack('3i', sock.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, 12))
    if uid != os.getuid():
        raise LinkError(Code.AUTH_FAILED, 'Control peer must be the profile owner.')


def request(directory: Path, action: str, **arguments):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    deadline = time.monotonic() + 3
    try:
        sock.settimeout(3)
        sock.connect(str(directory / 'control.sock'))
        check_peer(sock)
        send(sock, {'action': action, **arguments}, deadline)
        result = receive(sock, deadline)
    except (OSError, TimeoutError, ConnectionError):
        raise LinkError(Code.WORKER_UNAVAILABLE, 'Private broker is unavailable. Start `hermes workbench-link serve` in this profile.') from None
    finally:
        sock.close()
    if result.get('ok') is not True:
        try:
            code = Code(result['code'])
        except (KeyError, ValueError):
            code = Code.INTEGRITY_FAILURE
        raise LinkError(code, result.get('message', 'Invalid broker response.'), result.get('operation_id'))
    return result
