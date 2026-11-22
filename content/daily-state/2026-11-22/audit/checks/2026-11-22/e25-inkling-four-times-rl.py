import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e25-inkling-four-times-rl', 'artifact': 'episode', 'type': 'comparison', 'story': 'Nathan Lambert Cornell talk', 'quote': 'roughly four times as much for Inkling 2 Small'}


def check(ctx):
    return ctx.require('lambert', r'Inkling 2 Small', r'~4×')


if __name__ == '__main__':
    run_cli(CLAIM, check)
