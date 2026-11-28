import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe8-vendor-demo', 'artifact': 'episode', 'type': 'objection', 'story': 'Unsloth demos', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'First-party open-source repository README')
    if not ctx.art_has(r'(?is)(?:Unsloth(?:AI)?(?:.s own)?|the vendor) (?:demonstrated|demoed|showed|reports|says)|(?:vendor|first.party)[- ](?:reported|demo)'): return ctx.fail('framing', q, 'Present autonomy as a first-party demonstration, not an independent reliability result.')
    return ctx.ok('framing', q)


if __name__ == '__main__':
    run_cli(CLAIM, check)
