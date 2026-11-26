import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e09-like-count', 'artifact': 'episode', 'type': 'number', 'story': 'RSA rumors', 'quote': 'Viral posts with thousands of likes'}


def check(ctx):
    for a in ('andrewcurran_', 'kimmonismus'):
        q = ctx.find(a, r'^@(AndrewCurran_|kimmonismus)\s*\((?:[1-9]\d{3,}|[1-9]\d{0,2}(?:,\d{3})+|[1-9]\d*(?:\.\d+)?K) likes\)')
        if not q: return ctx.need(a, None, 'Original-post like count missing; reply counts do not count.')
    return ctx.ok(a, q, 'Both original posts meet the threshold.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
