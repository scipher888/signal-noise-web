import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot7-warning-hearsay', 'artifact': 'takeaways', 'type': 'objection', 'story': 'RSA rumors', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'only what he says he has heard')
    p = r'(?:Aaronson|he (?:wrote|said|says))[^.!?]{0,160}(?:heard|second[ -]hand|from multiple reliable sources)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'Attribute the warning to what Aaronson heard.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
