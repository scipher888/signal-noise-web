import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e11-riemann', 'artifact': 'episode', 'type': 'attribution', 'story': 'Math proofs', 'quote': 'fresh off an Anthropic-assisted Riemann Hypothesis proof'}


def check(ctx):
    return ctx.require('framing', r'Anthropic.{0,70}(?:assisted|helped).{0,70}(?:proof of the Riemann hypothesis|Riemann hypothesis proof)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
