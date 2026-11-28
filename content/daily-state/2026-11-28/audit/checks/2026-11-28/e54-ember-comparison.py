import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e54-ember-comparison', 'artifact': 'episode', 'type': 'comparison', 'story': 'Astra benchmarks', 'quote': 'more than doubles the previous high on the Ember-0 robotics benchmark'}


def check(ctx):
    return ctx.require('thezvi', r'robotics benchmark Ember-0, 41% versus a previous high of 20%')


if __name__ == '__main__':
    run_cli(CLAIM, check)
