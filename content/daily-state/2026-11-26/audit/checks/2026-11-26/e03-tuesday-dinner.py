import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e03-tuesday-dinner', 'artifact': 'episode', 'type': 'attribution', 'story': 'Aaronson dinner', 'quote': 'On Tuesday night, computer scientist Scott Aaronson had friends and colleagues over for dinner'}


def check(ctx):
    return ctx.require('framing', r'(?=.*Tuesday (?:night|evening))(?=.*Aaronson)(?=.*friends)(?=.*colleagues)(?=.*dinner)', note='Need the dinner account, not just a reference to his blog.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
