import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe8-logrank-epsilon', 'artifact': 'episode', 'type': 'objection', 'story': 'Google papers', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'epsilon of 5 millionths')
    return ctx.ok('framing', q) if ctx.art_has(r'\b(?:(?:five|5)[ -]millionths|0\.000005|5\s*(?:[×x]\s*10\^?|e)[−-]6)\b') else ctx.fail('framing', q, 'Quantify the claimed exponent improvement: five millionths.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
