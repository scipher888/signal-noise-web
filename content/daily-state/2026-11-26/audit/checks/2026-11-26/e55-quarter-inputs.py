import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e55-quarter-inputs', 'artifact': 'episode', 'type': 'number', 'story': 'Production verification', 'quote': 'it matched only about a quarter of live production inputs'}


def check(ctx):
    return ctx.require('anthropic', r'only about a quarter of inputs matched on production traffic')


if __name__ == '__main__':
    run_cli(CLAIM, check)
