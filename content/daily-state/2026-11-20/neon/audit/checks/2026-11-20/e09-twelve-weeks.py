import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e09-twelve-weeks', 'artifact': 'episode', 'type': 'number', 'story': 'Society', 'quote': 'Over twelve weeks'}


def check(ctx):
    return ctx.require('society', r'twelve-week study')


if __name__ == '__main__':
    run_cli(CLAIM, check)
