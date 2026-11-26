import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e14-exponent-value', 'artifact': 'episode', 'type': 'number', 'story': 'Math proofs', 'quote': 'the exact exponent of matrix multiplication is nine-fourths'}


def check(ctx):
    return ctx.require('framing', r'exact exponent of matrix multiplication.{0,20}(?:9/4|nine.fourths|2\.25)\b')


if __name__ == '__main__':
    run_cli(CLAIM, check)
