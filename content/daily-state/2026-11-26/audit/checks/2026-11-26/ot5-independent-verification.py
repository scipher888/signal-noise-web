import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot5-independent-verification', 'artifact': 'takeaways', 'type': 'objection', 'story': 'Gemini math papers', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'no independent verification is reported')
    return ctx.ok('framing', q) if ctx.art_has(r'no independent verification|not (?:yet )?independently verified|they remain unverified') else ctx.fail('framing', q, 'Flag lack of independent verification of the public claims.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
