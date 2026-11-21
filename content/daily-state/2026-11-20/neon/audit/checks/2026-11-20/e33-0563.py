import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e33-0563', 'artifact': 'episode', 'type': 'number', 'story': 'Airbnb', 'quote': 'Out of the box, that two-billion-parameter model scored a weak 0.563'}


def check(ctx):
    return ctx.require('airbnb', r'2 billion effective parameters', r'lifts its F1 from 0\.563')


if __name__ == '__main__':
    run_cli(CLAIM, check)
