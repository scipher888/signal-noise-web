import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's03-nine-to-sixteen-minutes', 'artifact': 'short', 'type': 'number', 'story': 'AI Autonomous Horizons', 'quote': 'nine to sixteen minutes'}


def check(ctx):
    return ctx.require('naam', r'nine minutes.*16 minutes')


if __name__ == '__main__':
    run_cli(CLAIM, check)
