import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's20-proof-checker-magic-opinion', 'artifact': 'short', 'type': 'opinion', 'story': 'AI Verification & Riemann Proof', 'quote': 'Anywhere you can build a proof checker, AI feels like magic.'}


def check(ctx):
    return ctx.need(None, None, 'Editorial opinion')


if __name__ == '__main__':
    run_cli(CLAIM, check)
