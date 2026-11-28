import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e68-human-intent', 'artifact': 'episode', 'type': 'attribution', 'story': 'Astra feedback', 'quote': 'misses obvious human intent'}


def check(ctx):
    return ctx.require('thezvi', r'takes you far too literally and does not understand human intent whatsoever', note='Practitioner assessment.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
