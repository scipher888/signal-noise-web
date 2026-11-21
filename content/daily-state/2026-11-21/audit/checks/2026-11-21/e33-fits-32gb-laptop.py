import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e33-fits-32gb-laptop', 'artifact': 'episode', 'type': 'number', 'story': 'Inkling 2 Mini', 'quote': 'fits on a thirty-two-gigabyte laptop'}


def check(ctx):
    return ctx.require('thinking', r'MacBook.*at least 32GB RAM')


if __name__ == '__main__':
    run_cli(CLAIM, check)
