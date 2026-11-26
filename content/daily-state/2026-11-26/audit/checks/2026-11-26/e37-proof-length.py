import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e37-proof-length', 'artifact': 'episode', 'type': 'number', 'story': 'Proof verification', 'quote': 'can span hundreds of thousands or millions of lines'}


def check(ctx):
    return ctx.require('framing', r'(?:machine.checked|formalized) proofs.{0,70}hundreds of thousands or millions of lines')


if __name__ == '__main__':
    run_cli(CLAIM, check)
