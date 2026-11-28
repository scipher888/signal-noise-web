import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e78-browser-score', 'artifact': 'episode', 'type': 'number', 'story': 'Model routing', 'quote': '82 percent'}


def check(ctx):
    return ctx.require('thezvi', r'GPT-6\.2 Sol is the new top model for browser use at 82%')


if __name__ == '__main__':
    run_cli(CLAIM, check)
