import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't08-17-million-line', 'artifact': 'takeaways', 'type': 'number', 'story': 'Riemann Hypothesis Lean proof', 'quote': '17-million-line'}


def check(ctx):
    return ctx.require('lean', r'17 million lines of code')


if __name__ == '__main__':
    run_cli(CLAIM, check)
