import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e07-laptop-sized-model-tml', 'artifact': 'episode', 'type': 'attribution', 'story': 'Inkling 2 Mini', 'quote': 'a new laptop-sized model released by Thinking Machines Lab'}


def check(ctx):
    return ctx.require('thinking', r'Thinking Machines Lab', r'releasing Inkling 2 Mini.*small enough to run on your laptop')


if __name__ == '__main__':
    run_cli(CLAIM, check)
