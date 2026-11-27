import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e22-error-log', 'artifact': 'episode', 'type': 'attribution', 'story': 'METR chart debate', 'quote': "noting that flashy headline figures will likely earn a new item on METR's internal publication error log"}


def check(ctx):
    return ctx.require('bethmaybarnes', r'we keep a .publication error log.*probably end up as an item on there.*flashy graph or numerical claim')


if __name__ == '__main__':
    run_cli(CLAIM, check)
