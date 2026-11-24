import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e23-shirudo-ebpf-runtime', 'artifact': 'episode', 'type': 'attribution', 'story': 'Linux Cybersecurity', 'quote': 'a Linux runtime that lets agents write temporary, cryptographically signed eBPF shields to block exploits on running servers without a restart'}


def check(ctx):
    return ctx.require('openai', r'eBPF shields', r'cryptographically signed', note='Primary Shirudo source not in snapshot')


if __name__ == '__main__':
    run_cli(CLAIM, check)
