import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e29-metr-improving-high-cost-tasks', 'artifact': 'episode', 'type': 'qualifier', 'story': 'METR capability update', 'quote': "METR's data shows models are improving even on high-cost tasks, just from a lower baseline"}


def check(ctx):
    return ctx.require('metr', r'AI performance improving over time even on our most costly tasks', r'models perform worse on the higher Lifecycle Cost subset')


if __name__ == '__main__':
    run_cli(CLAIM, check)
