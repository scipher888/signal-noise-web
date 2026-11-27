import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't07-internal-disagreement', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Pretraining loss', 'quote': 'the group stressed its own staff disagreed on what the data means'}


def check(ctx):
    return ctx.require('metr', r'Among METR staff there remains active discussion on how to interpret', r'substantial disagreements.*METR does not have a consensus view')


if __name__ == '__main__':
    run_cli(CLAIM, check)
