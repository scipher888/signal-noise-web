import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e02-anthropic-mathematician-riemann', 'artifact': 'episode', 'type': 'attribution', 'story': 'Riemann Hypothesis proof', 'quote': 'a mathematician at Anthropic says he and Claude may have just proved the Riemann Hypothesis'}


def check(ctx):
    s1 = ctx.find('alpoge', r'working with Claude, discovered a proof')
    s2 = ctx.find('andrewcurran_', r'Levent Alpöge at Anthropic')
    if s1 and s2:
        return ctx.ok('alpoge', s1, 'Anthropic affiliation confirmed via andrewcurran_')
    return ctx.need('alpoge', s1 or s2, 'Could not verify both proof claim and Anthropic affiliation')


if __name__ == '__main__':
    run_cli(CLAIM, check)
