import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e12-azspc-96-98-percentile', 'artifact': 'episode', 'type': 'number', 'story': 'METR capability update', 'quote': 'They hit the 96th to 98th percentile in multi-month Al Zimmermann programming contests'}


def check(ctx):
    return ctx.require('metr', r'Al Zimmermann contests, multi-month', r'96th to 98th percentile')


if __name__ == '__main__':
    run_cli(CLAIM, check)
