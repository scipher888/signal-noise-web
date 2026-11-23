import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'os3-lambert-slides-not-peer-reviewed', 'artifact': 'short', 'type': 'objection', 'story': 'AI Verification & Riemann Proof', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'opinion and research agenda, not peer-reviewed findings')
    if not ctx.art_has(r'not.*peer[- ]review|opinion|research agenda|author.s own'):
        return ctx.fail('framing', q, 'Short omits Lambert framing caveat: author talk slides representing opinion and research agenda, not peer-reviewed findings')
    return ctx.ok('framing', q)


if __name__ == '__main__':
    run_cli(CLAIM, check)
