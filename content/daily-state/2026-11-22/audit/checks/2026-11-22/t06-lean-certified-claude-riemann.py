import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't06-lean-certified-claude-riemann', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Riemann Hypothesis Lean proof', 'quote': "The Lean and Mathlib communities certified Levent Alpöge's Claude-assisted, 17-million-line Lean proof of the Riemann Hypothesis"}


def check(ctx):
    q = ctx.find('lean', r'Levent Alpöge released a proof of the Riemann Hypothesis as a Lean library comprising 17 million lines of code')
    if ctx.find('lean', r'Claude'):
        return ctx.ok('lean', q)
    return ctx.need('lean', q, 'Primary source lean confirms certification of Alpöge 17M-line proof but does not mention Claude')


if __name__ == '__main__':
    run_cli(CLAIM, check)
