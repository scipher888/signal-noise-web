import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e10-rh-grh-without-assumptions', 'artifact': 'episode', 'type': 'attribution', 'story': 'Riemann Hypothesis proof', 'quote': 'claiming he and Claude discovered a proof of the Riemann Hypothesis, and even the Generalized Riemann Hypothesis, formalized without assumptions'}


def check(ctx):
    return ctx.require('alpoge', r'working with Claude, discovered a proof', r'Generalized Riemann Hypothesis', r'formalized the arguments without assumptions')


if __name__ == '__main__':
    run_cli(CLAIM, check)
