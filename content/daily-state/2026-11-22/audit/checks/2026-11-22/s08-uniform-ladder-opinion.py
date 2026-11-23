import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's08-uniform-ladder-opinion', 'artifact': 'short', 'type': 'opinion', 'story': 'AI Verification & Riemann Proof', 'quote': "AI isn't climbing a uniform ladder of intelligence."}


def check(ctx):
    return ctx.need(None, None, 'Editorial synthesis/opinion')


if __name__ == '__main__':
    run_cli(CLAIM, check)
