import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e40-hit-rate', 'artifact': 'episode', 'type': 'number', 'story': 'Protein design', 'quote': 'an 11 percent hit rate'}


def check(ctx):
    return ctx.require('openai', r'35 \(10\.9%\) tested positive for binding', note='10.9% rounds to 11%.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
