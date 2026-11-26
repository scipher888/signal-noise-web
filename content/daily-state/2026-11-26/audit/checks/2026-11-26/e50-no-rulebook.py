import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e50-no-rulebook', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Production verification', 'quote': 'There is no fixed rulebook'}


def check(ctx):
    return ctx.require('anthropic', r'In our case, neither approach was sufficient', r'definition of .correct. a moving target', note='Supports the claim for this migration, not every production system.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
