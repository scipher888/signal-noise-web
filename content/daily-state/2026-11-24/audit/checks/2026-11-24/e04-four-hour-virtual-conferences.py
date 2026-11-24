import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e04-four-hour-virtual-conferences', 'artifact': 'episode', 'type': 'number', 'story': 'Quantum Circuits', 'quote': 'Every four hours, separate agent teams met in virtual conferences to debate and trade ideas'}


def check(ctx):
    return ctx.require('deepmind', r'separate, independent agent teams', r'Every four hours, agents from each team met at a virtual conference to trade, debate')


if __name__ == '__main__':
    run_cli(CLAIM, check)
