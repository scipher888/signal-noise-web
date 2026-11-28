import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot4-company-benchmarks', 'artifact': 'takeaways', 'type': 'objection', 'story': 'Benchmarks and builder reports', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'Company-reported launch benchmarks')
    if not ctx.art_has(r'(?is)(?:OpenAI[- ]reported|OpenAI reports|company[- ]reported).{0,80}(?:benchmarks?|highs)'): return ctx.fail('framing', q, 'Attribute company results separately from ARC verification.')
    return ctx.ok('framing', q)


if __name__ == '__main__':
    run_cli(CLAIM, check)
