import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's02-claude-assisted-riemann', 'artifact': 'short', 'type': 'attribution', 'story': 'AI Verification & Riemann Proof', 'quote': 'Claude-assisted proof of the Riemann Hypothesis'}


def check(ctx):
    q = ctx.find('lean', r'proof of the Riemann Hypothesis')
    if ctx.find('lean', r'Claude'):
        return ctx.ok('lean', q)
    return ctx.need('lean', q, 'Primary source lean does not mention Claude')


if __name__ == '__main__':
    run_cli(CLAIM, check)
