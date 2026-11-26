import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e37-no-announcement', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Google papers', 'quote': 'with no announcement'}


def check(ctx):
    return ctx.require('framing', r'(?=.*Google)(?=.*(?:without (?:an |any )?announcement|no announcement|unannounced))', note='Public posting alone cannot decide whether it was announced.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
