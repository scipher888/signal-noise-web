import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e77-browser-lead', 'artifact': 'episode', 'type': 'comparison', 'story': 'Model routing', 'quote': 'leads Browser Use at 82 percent'}


def check(ctx):
    return ctx.require('thezvi', r'Browser Use finds that GPT-6\.2 Sol is the new top model for browser use at 82%')


if __name__ == '__main__':
    run_cli(CLAIM, check)
