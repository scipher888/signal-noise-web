import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e16-not-mastered-neighborhoods', 'artifact': 'episode', 'type': 'attribution', 'story': 'Riemann Hypothesis proof', 'quote': 'openly admitting he is presenting a complete proof before he has even mastered huge neighborhoods of its own mathematics'}


def check(ctx):
    return ctx.require('alpoge', r'presenting the world with a complete argument before having mastered a massive neighbourhood')


if __name__ == '__main__':
    run_cli(CLAIM, check)
