import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e61-game-of-telephone', 'artifact': 'episode', 'type': 'attribution', 'story': 'Aaronson crypto warning', 'quote': 'warning that technical specifics were likely getting mangled in a game of telephone'}


def check(ctx):
    return ctx.require('framing', r'(?=.*Aaronson)(?=.*(?:specifics|details))(?=.*(?:likely|probably))(?=.*(?:mangled|distorted|game of telephone))')


if __name__ == '__main__':
    run_cli(CLAIM, check)
