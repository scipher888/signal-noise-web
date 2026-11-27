import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot2-company-docs', 'artifact': 'takeaways', 'type': 'objection', 'story': 'Claude refusal behavior', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'Company documentation of refusal categories')
    return ctx.ok('framing', q) if ctx.art_has(r'Anthropic.s (?:own )?(?:API|developer|platform) doc') else ctx.fail('framing', q, 'Identify the source as company documentation.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
