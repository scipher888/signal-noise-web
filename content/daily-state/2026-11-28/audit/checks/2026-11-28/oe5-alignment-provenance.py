import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe5-alignment-provenance', 'artifact': 'episode', 'type': 'objection', 'story': 'Alignment evaluations', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'self-reported alignment/safety evaluations')
    if not ctx.art_has(r'(?is)(?:OpenAI.s own|OpenAI[- ]reported|self[- ]reported|OpenAI says).{0,70}(?:alignment|safety evaluations)'): return ctx.fail('framing', q, 'Identify who conducted the alignment evaluations.')
    return ctx.ok('framing', q)


if __name__ == '__main__':
    run_cli(CLAIM, check)
