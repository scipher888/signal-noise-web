import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e67-hard-problems', 'artifact': 'episode', 'type': 'attribution', 'story': 'Astra feedback', 'quote': 'Astra solves brutal math, physics, and 3D challenges'}


def check(ctx):
    return ctx.require('thezvi', r'Very good at hard math/science/3D', r'(?:solv|hard|challenge).*physics|physics.*(?:solv|challenge)', note='A broad science endorsement does not identify a solved physics challenge.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
