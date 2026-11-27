import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe7-no-record', 'artifact': 'episode', 'type': 'objection', 'story': 'Claude sabotage allegations', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'Schirano shared no transcript or log')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:no|none|without|did not|didn.t)[^.]{0,100}(?:transcripts?|logs?)') else ctx.fail('framing', q, 'State that no transcript or log was shared.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
