import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e03-17m-lines-lean', 'artifact': 'episode', 'type': 'number', 'story': 'Riemann Hypothesis proof', 'quote': '17 million lines of Lean code'}


def check(ctx):
    return ctx.require('lean', r'Lean library comprising 17 million lines of code')


if __name__ == '__main__':
    run_cli(CLAIM, check)
