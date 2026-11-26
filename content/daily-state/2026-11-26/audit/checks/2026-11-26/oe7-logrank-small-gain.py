import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe7-logrank-small-gain', 'artifact': 'episode', 'type': 'objection', 'story': 'Google papers', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'tiny improvement over the square-root bound')
    p = r'(?:tiny|small|slight|modest|marginal)[^.!?]{0,70}(?:square[ -]root|sqrt)|(?:square[ -]root|sqrt)[^.!?]{0,70}(?:tiny|small|slight|modest|marginal)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'Describe the log-rank result as a small improvement over the square-root bound.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
