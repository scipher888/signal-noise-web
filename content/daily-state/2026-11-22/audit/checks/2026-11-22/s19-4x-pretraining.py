import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's19-4x-pretraining', 'artifact': 'short', 'type': 'number', 'story': 'AI Verification & Riemann Proof', 'quote': '4x pretraining'}


def check(ctx):
    return ctx.require('lambert', r'Inkling 2 Small', r'~4×')


if __name__ == '__main__':
    run_cli(CLAIM, check)
