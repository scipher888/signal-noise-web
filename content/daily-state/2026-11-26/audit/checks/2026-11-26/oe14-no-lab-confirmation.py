import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe14-no-lab-confirmation', 'artifact': 'episode', 'type': 'objection', 'story': 'RSA rumors', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'No lab has published or confirmed such a result')
    p = r'(?:no (?:frontier )?labs? (?:has |have )?(?:published or )?(?:publicly )?confirmed|no lab confirmation|not (?:been )?confirmed by (?:any|either|the) labs?|neither lab has confirmed)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'Explicitly state no lab confirmation; unreleased does not mean unconfirmed.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
