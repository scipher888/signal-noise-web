import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's05-9-to-16-min', 'artifact': 'short', 'type': 'number', 'story': 'AI Autonomous Horizons', 'quote': '9–16 min'}


def check(ctx):
    return ctx.require('naam', r'nine minutes.*16 minutes')


if __name__ == '__main__':
    run_cli(CLAIM, check)
