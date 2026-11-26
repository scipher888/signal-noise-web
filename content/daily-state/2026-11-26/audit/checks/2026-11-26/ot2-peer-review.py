import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot2-peer-review', 'artifact': 'takeaways', 'type': 'objection', 'story': 'Gemini math papers', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'no peer review')
    return ctx.ok('framing', q) if ctx.art_has(r'no peer review|not (?:yet )?peer[- ]reviewed|without peer review|awaiting peer review') else ctx.fail('framing', q, 'State lack of peer review.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
