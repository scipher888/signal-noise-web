import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe11-warning-hearsay', 'artifact': 'episode', 'type': 'objection', 'story': 'Aaronson crypto warning', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'only what he says he has heard')
    p = r'(?:Aaronson|he (?:wrote|said|says))[^.!?]{0,160}(?:heard|second[ -]hand|from multiple reliable sources)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'Identify the warning as what Aaronson reports hearing.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
