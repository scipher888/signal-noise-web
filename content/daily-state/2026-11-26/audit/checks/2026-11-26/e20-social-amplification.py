import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e20-social-amplification', 'artifact': 'episode', 'type': 'attribution', 'story': 'Factoring rumor', 'quote': 'social accounts amplified an unverified ten-day rumor'}


def check(ctx):
    q = ctx.find('kimmonismus', r'aggregator account amplifying a rumor; no independent sourcing and no lab confirmation')
    d = ctx.find('andrewcurran_', r'this rumor has persisted for about ten days, about both Anthropic and OpenAI')
    return ctx.ok('kimmonismus', q, str(d)) if q and d else ctx.need('andrewcurran_', d, 'Need both duration and evidence of unconfirmed amplification.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
