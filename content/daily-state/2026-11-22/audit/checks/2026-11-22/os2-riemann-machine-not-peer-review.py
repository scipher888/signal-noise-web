import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'os2-riemann-machine-not-peer-review', 'artifact': 'short', 'type': 'objection', 'story': 'AI Verification & Riemann Proof', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'machine verification of a formal proof, not a human-readable paper or journal peer review')
    if not ctx.art_has(r'not.*peer[- ]review|not.*human[- ]readable|not.*journal|machine verif.*not|formal.*not.*paper|nobody has read|human-readable'):
        return ctx.fail('framing', q, 'Short omits Riemann framing caveat: machine verification of a formal proof, not a human-readable paper or journal peer review')
    return ctx.ok('framing', q)


if __name__ == '__main__':
    run_cli(CLAIM, check)
