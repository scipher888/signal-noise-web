import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e34-four-previous', 'artifact': 'episode', 'type': 'number', 'story': 'Google papers', 'quote': 'four AI-generated papers over the previous month'}


def check(ctx):
    return ctx.require('framing', r'(?=.*Google)(?=.*(?:four|4) (?:AI-generated|Cogentic) papers)(?=.*(?:last|previous|preceding) month)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
