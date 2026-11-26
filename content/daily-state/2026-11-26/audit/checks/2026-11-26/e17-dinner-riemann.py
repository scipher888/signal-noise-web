import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e17-dinner-riemann', 'artifact': 'episode', 'type': 'attribution', 'story': 'Aaronson dinner', 'quote': "Aaronson's dinner guests were still absorbing last week's Alpöge and Anthropic proof of the Riemann Hypothesis"}


def check(ctx):
    return ctx.require('framing', r'(?=.*(?:dinner|guests))(?=.*last week)(?=.*Alpöge)(?=.*Anthropic)(?=.*proof of the Riemann [Hh]ypothesis)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
