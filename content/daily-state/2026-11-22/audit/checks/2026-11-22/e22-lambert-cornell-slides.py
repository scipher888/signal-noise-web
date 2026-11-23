import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e22-lambert-cornell-slides', 'artifact': 'episode', 'type': 'attribution', 'story': 'Nathan Lambert Cornell talk', 'quote': "Nathan Lambert's new Cornell slides"}


def check(ctx):
    return ctx.require('lambert', r'Nathan Lambert', r'Cornell University, November 20, 2026', r'Slides:')


if __name__ == '__main__':
    run_cli(CLAIM, check)
