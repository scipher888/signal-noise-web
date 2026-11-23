import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e01-episode-date', 'artifact': 'episode', 'type': 'number', 'story': 'Episode date', 'quote': 'November 21st, 2026'}


def check(ctx):
    return ctx.require('naam', r'Nov 21, 2026')


if __name__ == '__main__':
    run_cli(CLAIM, check)
