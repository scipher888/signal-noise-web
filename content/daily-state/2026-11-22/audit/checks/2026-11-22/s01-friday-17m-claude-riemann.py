import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's01-friday-17m-claude-riemann', 'artifact': 'short', 'type': 'number', 'story': 'AI Verification & Riemann Proof', 'quote': 'On Friday, a 17-million-line, Claude-assisted proof of the Riemann Hypothesis dropped'}


def check(ctx):
    q = ctx.find('lean', r'November 20, 2026.*17 million lines of code')
    if ctx.find('lean', r'Claude'):
        return ctx.ok('lean', q)
    return ctx.need('lean', q, 'Primary source lean confirms 17 million lines released Nov 20 (Friday) but does not mention Claude')


if __name__ == '__main__':
    run_cli(CLAIM, check)
