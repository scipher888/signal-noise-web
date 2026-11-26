import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot4-factoring-bound', 'artifact': 'takeaways', 'type': 'objection', 'story': 'Gemini math papers', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'subexponential, not polynomial')
    return ctx.ok('framing', q) if ctx.art_has(r'sub[- ]?exponential.{0,50}(?:not|rather than) polynomial|not polynomial.{0,50}sub[- ]?exponential') else ctx.fail('framing', q, 'Give the qualification on the public factoring bound.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
