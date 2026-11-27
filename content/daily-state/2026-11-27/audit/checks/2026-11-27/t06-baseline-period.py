import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't06-baseline-period', 'artifact': 'takeaways', 'type': 'number', 'story': 'Pretraining loss', 'quote': 'in 2022 through 2025'}


def check(ctx):
    return ctx.require('metr', r'about seven times faster than it was from 2022 through 2025')


if __name__ == '__main__':
    run_cli(CLAIM, check)
