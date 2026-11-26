import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e18-riemann-proof', 'artifact': 'episode', 'type': 'attribution', 'story': 'Riemann Hypothesis', 'quote': "last week's Alpöge and Anthropic proof of the Riemann Hypothesis"}


def check(ctx):
    return ctx.require('framing', r'(?=.*last week)(?=.*Alpöge)(?=.*Anthropic)(?=.*(?:proved the|proof of the) Riemann hypothesis)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
