import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe3-no-peer-review', 'artifact': 'episode', 'type': 'objection', 'story': 'Google papers', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'no peer review')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:no peer review|(?:not(?: yet)?|non|not been)[ -]peer[ -]reviewed|await(?:ing)? peer review)') else ctx.fail('framing', q, 'State that the preprints lack peer review.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
