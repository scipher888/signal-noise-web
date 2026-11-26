import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e28-single-framework', 'artifact': 'episode', 'type': 'number', 'story': 'Tensor geometry', 'quote': 'A single new framework built on tensor geometry powered multiple major results at once'}


def check(ctx):
    return ctx.require('framing', r'(?=.*(?:single|one|same) new framework)(?=.*tensor geometry)(?=.*(?:both|multiple|several) .*results)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
