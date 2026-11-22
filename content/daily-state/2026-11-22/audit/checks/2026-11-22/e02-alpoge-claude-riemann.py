import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e02-alpoge-claude-riemann', 'artifact': 'episode', 'type': 'attribution', 'story': 'Riemann Hypothesis proof', 'quote': 'Levent Alpöge released a Claude-assisted proof of the Riemann Hypothesis'}


def check(ctx):
    q = ctx.find('lean', r'Levent Alpöge released a proof of the Riemann Hypothesis')
    if not q:
        return ctx.need('lean', None, 'Alpöge release sentence not found in lean')
    if ctx.find('lean', r'Claude'):
        return ctx.ok('lean', q)
    return ctx.need('lean', q, 'Primary source lean confirms Alpöge released the proof but does not mention Claude')


if __name__ == '__main__':
    run_cli(CLAIM, check)
