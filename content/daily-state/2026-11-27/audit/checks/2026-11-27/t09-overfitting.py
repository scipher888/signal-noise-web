import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't09-overfitting', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Pretraining loss', 'quote': 'possible overfitting'}


def check(ctx):
    return ctx.require('metr', r'It is possible that the data released overstates true progress in pretraining', r'through various types of overfitting')


if __name__ == '__main__':
    run_cli(CLAIM, check)
