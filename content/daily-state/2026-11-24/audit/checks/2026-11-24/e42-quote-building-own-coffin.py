import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e42-quote-building-own-coffin', 'artifact': 'episode', 'type': 'quote', 'story': 'Anthropic Enterprise Study', 'quote': 'as one put it, like they are building their own coffin'}


def check(ctx):
    return ctx.require('anthropic', r'building my own coffin')


if __name__ == '__main__':
    run_cli(CLAIM, check)
