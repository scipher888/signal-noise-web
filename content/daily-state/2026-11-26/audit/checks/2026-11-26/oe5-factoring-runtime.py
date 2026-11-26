import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe5-factoring-runtime', 'artifact': 'episode', 'type': 'objection', 'story': 'Google factoring', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'subexponential, not polynomial')
    p = r'(?:subexponential[^.!?]{0,110}(?:not|rather than|instead of) (?:a )?polynomial|not polynomial[^.!?]{0,110}subexponential)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'Distinguish the claimed subexponential bound from a polynomial one.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
