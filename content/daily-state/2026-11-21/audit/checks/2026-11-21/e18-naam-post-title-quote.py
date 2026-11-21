import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e18-naam-post-title-quote', 'artifact': 'episode', 'type': 'quote', 'story': 'AI task-horizon analysis', 'quote': 'The Most Important Charts in AI are Wrong'}


def check(ctx):
    return ctx.require('naam', r'The Most Important Charts in AI are Wrong')


if __name__ == '__main__':
    run_cli(CLAIM, check)
