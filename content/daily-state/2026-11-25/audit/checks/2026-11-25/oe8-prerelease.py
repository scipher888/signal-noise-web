import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe8-prerelease', 'artifact': 'episode', 'type': 'objection', 'story': 'Chabot sketchbook', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'he tested the model before release')
    return ctx.ok('framing', q) if ctx.art_has(r'(?is)(?:Humphries|historian|sketchbook).{0,120}(?:pre[- ]?release|before (?:its |public )?release|before it was released|early access)|(?:pre[- ]?release|early access).{0,60}(?:Astra|Humphries)') else ctx.fail('framing', q, 'Mention the historian’s prerelease access.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
