import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e53-ember-roundup', 'artifact': 'episode', 'type': 'attribution', 'story': 'Astra benchmarks', 'quote': "Zvi Mowshowitz's roundup notes it more than doubles the previous high on the Ember-0 robotics benchmark at 41 percent"}


def check(ctx):
    return ctx.require('thezvi', r'Astra aces robotics benchmark Ember-0, 41% versus a previous high of 20%', note='41 > 2 × 20; attribution is to the roundup.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
