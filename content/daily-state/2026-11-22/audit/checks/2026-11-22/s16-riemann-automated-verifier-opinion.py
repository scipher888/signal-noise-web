import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's16-riemann-automated-verifier-opinion', 'artifact': 'short', 'type': 'opinion', 'story': 'AI Verification & Riemann Proof', 'quote': 'Riemann fell because Lean turns pure math into an automated verifier.'}


def check(ctx):
    return ctx.need(None, None, 'Editorial interpretation/opinion')


if __name__ == '__main__':
    run_cli(CLAIM, check)
