import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e53-weakened-assertions', 'artifact': 'episode', 'type': 'number', 'story': 'Production verification', 'quote': 'an audit found over a hundred weakened assertions'}


def check(ctx):
    return ctx.require('anthropic', r'when we audited the ported tests, we found more than 100 weakened assertions')


if __name__ == '__main__':
    run_cli(CLAIM, check)
