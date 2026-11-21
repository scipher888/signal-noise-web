import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e20-10of16', 'artifact': 'episode', 'type': 'number', 'story': 'Society', 'quote': 'flagged ten of sixteen repaired versions where the limitation was already openly disclosed'}


def check(ctx):
    return ctx.require('society', r'10 of 16 repaired versions in which the limitation was already openly disclosed')


if __name__ == '__main__':
    run_cli(CLAIM, check)
