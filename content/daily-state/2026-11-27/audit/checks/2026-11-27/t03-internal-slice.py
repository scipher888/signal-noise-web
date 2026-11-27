import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't03-internal-slice', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Pretraining loss', 'quote': 'on an internal codebase slice'}


def check(ctx):
    return ctx.require('metr', r'reports loss on a corpus sourced from its own internal codebase')


if __name__ == '__main__':
    run_cli(CLAIM, check)
