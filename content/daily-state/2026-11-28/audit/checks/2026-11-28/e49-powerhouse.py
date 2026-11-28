import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e49-powerhouse', 'artifact': 'episode', 'type': 'opinion', 'story': 'Astra benchmarks', 'quote': 'On paper, Astra is a powerhouse'}


def check(ctx):
    return ctx.need('gpt', ctx.find('gpt', r'Astra sets a new high, scoring'), 'Powerhouse is an assessment, not a benchmark threshold.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
