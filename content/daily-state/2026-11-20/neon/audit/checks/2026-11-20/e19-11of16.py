import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e19-11of16', 'artifact': 'episode', 'type': 'number', 'story': 'Society', 'quote': 'Text-only reviewers caught eleven of sixteen flawed drafts'}


def check(ctx):
    return ctx.require('society', r'Text-only reviewers flagged 11 of 16 flawed')


if __name__ == '__main__':
    run_cli(CLAIM, check)
