import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's19-26b-local', 'artifact': 'short', 'type': 'number', 'story': 'Inkling 2 Mini', 'quote': '26B local'}


def check(ctx):
    return ctx.require('thinking', r'26\.4B total parameters', r'run on local devices')


if __name__ == '__main__':
    run_cli(CLAIM, check)
