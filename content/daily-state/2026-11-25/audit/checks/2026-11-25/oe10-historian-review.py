import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe10-historian-review', 'artifact': 'episode', 'type': 'objection', 'story': 'Chabot sketchbook', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'no independent historian review is reported yet')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:Substack|attribution|sketchbook|historian.s account).{0,60}(?:not yet peer[- ]reviewed|not (?:yet )?independently (?:checked|reviewed)|no independent (?:historian )?review)|no independent historian review') else ctx.fail('framing', q, 'Disclose lack of reported independent review of the attribution.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
