import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot5-no-record', 'artifact': 'takeaways', 'type': 'objection', 'story': 'Claude refusal behavior', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'Schirano shared no transcript or log')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:no|none|without|did not|didn.t)[^.]{0,100}(?:transcripts?|logs?)') else ctx.fail('framing', q, 'Disclose lack of a transcript or log.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
