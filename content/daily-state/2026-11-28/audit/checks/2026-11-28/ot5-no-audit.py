import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot5-no-audit', 'artifact': 'takeaways', 'type': 'objection', 'story': 'Benchmarks and builder reports', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'not independently audited')
    if not ctx.art_has(r'(?is)(?:OpenAI|company|launch benchmarks).{0,180}(?:not (?:been )?independently audited|no independent audit|without an independent audit)'): return ctx.fail('framing', q, 'Company benchmark highs were not independently audited.')
    return ctx.ok('framing', q)


if __name__ == '__main__':
    run_cli(CLAIM, check)
