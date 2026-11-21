import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e13-steered-claude-outpaced', 'artifact': 'episode', 'type': 'attribution', 'story': 'Riemann Hypothesis proof', 'quote': 'He steered Claude toward the right analogy, and near the finish line, Claude outpaced him.'}


def check(ctx):
    return ctx.require('alpoge', r'guided us to the right situation analogous', r'Claude far outpaced me near the finish line')


if __name__ == '__main__':
    run_cli(CLAIM, check)
