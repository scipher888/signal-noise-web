import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's09-shipped-lean-code-compiler', 'artifact': 'short', 'type': 'attribution', 'story': 'Riemann Hypothesis Proof', 'quote': 'he just shipped Lean code for a compiler to check'}


def check(ctx):
    return ctx.require('alpoge', r'decided to only present Lean')


if __name__ == '__main__':
    run_cli(CLAIM, check)
