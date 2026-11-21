import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e12-9500', 'artifact': 'episode', 'type': 'number', 'story': 'Society', 'quote': 'exchanged 9,500 messages'}


def check(ctx):
    return ctx.require('society', r'exchanged 9,500 messages')


if __name__ == '__main__':
    run_cli(CLAIM, check)
