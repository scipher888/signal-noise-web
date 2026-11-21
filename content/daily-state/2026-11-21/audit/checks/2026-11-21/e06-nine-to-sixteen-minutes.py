import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e06-nine-to-sixteen-minutes', 'artifact': 'episode', 'type': 'number', 'story': 'AI task-horizon analysis', 'quote': 'nine to sixteen minutes'}


def check(ctx):
    return ctx.require('naam', r'nine minutes.*16 minutes')


if __name__ == '__main__':
    run_cli(CLAIM, check)
