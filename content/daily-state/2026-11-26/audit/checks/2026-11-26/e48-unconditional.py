import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e48-unconditional', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Google factoring', 'quote': 'One gives an unconditional algorithm without unproven number-theoretic assumptions'}


def check(ctx):
    return ctx.require('framing', r'(?=.*factoring)(?=.*unconditional)(?=.*(?:without|no) (?:unproven|unproved) number.theoretic assumptions)', note='Do not use the unconditional log-rank formalization.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
