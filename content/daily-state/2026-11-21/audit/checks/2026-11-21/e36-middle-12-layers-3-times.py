import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e36-middle-12-layers-3-times', 'artifact': 'episode', 'type': 'number', 'story': 'Inkling 2 Mini', 'quote': 'running its middle twelve layers three times per token'}


def check(ctx):
    return ctx.require('thinking', r'middle layers of the model three times for every token', r'looping the middle 12 layers')


if __name__ == '__main__':
    run_cli(CLAIM, check)
