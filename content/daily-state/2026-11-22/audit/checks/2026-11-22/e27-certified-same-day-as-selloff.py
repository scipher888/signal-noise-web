import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e27-certified-same-day-as-selloff', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Riemann Hypothesis proof', 'quote': 'a certified Riemann proof on the same day the stock market panics about AI returns'}


def check(ctx):
    q_rel = ctx.find('lean', r'On November 20, 2026, Levent Alpöge released')
    q_cert = ctx.find('lean', r'2026-11-21')
    if q_rel and q_cert:
        return ctx.fail('lean', q_rel, 'Proof was released Friday Nov 20 (when Nasdaq sold off) and certified Saturday Nov 21, not certified on the same trading day')
    return ctx.need('lean', q_rel, 'Could not verify release vs certification date')


if __name__ == '__main__':
    run_cli(CLAIM, check)
