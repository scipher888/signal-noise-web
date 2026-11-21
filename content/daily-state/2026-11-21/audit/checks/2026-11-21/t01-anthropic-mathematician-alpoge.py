import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't01-anthropic-mathematician-alpoge', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Riemann Hypothesis proof claim', 'quote': 'Anthropic mathematician Levent Alpöge'}


def check(ctx):
    return ctx.require('andrewcurran_', r'Levent Alpöge at Anthropic')


if __name__ == '__main__':
    run_cli(CLAIM, check)
