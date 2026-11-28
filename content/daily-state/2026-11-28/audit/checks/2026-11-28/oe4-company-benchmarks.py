import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe4-company-benchmarks', 'artifact': 'episode', 'type': 'objection', 'story': 'Astra benchmarks', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'Company-reported launch benchmarks, pricing')
    if not ctx.art_has(r'(?is)OpenAI(?:[- ]reported| reports| says| claims|.s own).{0,130}(?:evaluations|benchmarks|cost per task)'): return ctx.fail('framing', q, 'Distinguish company performance and cost claims from ARC verification.')
    return ctx.ok('framing', q)


if __name__ == '__main__':
    run_cli(CLAIM, check)
