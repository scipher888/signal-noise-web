import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot8-warning-specifics', 'artifact': 'takeaways', 'type': 'objection', 'story': 'RSA rumors', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'explicitly declines to vouch for the specifics')
    p = r'(?:(?:declin\w*|refus\w*|would not|did not)[^.!?]{0,80}(?:vouch|name RSA|claim[^.!?]{0,50}factor)|specifics[^.!?]{0,60}(?:uncertain|mangled))'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'Keep Aaronson’s disclaimer about specifics.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
