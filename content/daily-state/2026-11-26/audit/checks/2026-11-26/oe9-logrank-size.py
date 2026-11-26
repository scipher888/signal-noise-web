import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe9-logrank-size', 'artifact': 'episode', 'type': 'objection', 'story': 'Google papers', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'tiny improvement over the square-root bound')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:tiny|slight|small) improvement.{0,50}square[- ]root|(?:epsilon|exponent).{0,35}(?:five millionths|5 millionths|0\.000005)') else ctx.fail('framing', q, 'Describe the small improvement to the square-root bound.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
