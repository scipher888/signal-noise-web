import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot6-factoring-unverified', 'artifact': 'takeaways', 'type': 'objection', 'story': 'Cogentic papers', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'no independent verification is reported')
    p = r'(?:factor\w*[^.!?]{0,180}(?:no independent verification|not (?:yet )?(?:been )?independently verified|unverified)|(?:no independent verification|not independently verified|unverified)[^.!?]{0,180}factor\w*)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'No independent verification of the public factoring claim is reported.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
