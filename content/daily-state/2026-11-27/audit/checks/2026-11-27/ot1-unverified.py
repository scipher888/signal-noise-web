import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot1-unverified', 'artifact': 'takeaways', 'type': 'objection', 'story': 'Claude refusal behavior', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'verification_status: unverified_debate')
    return ctx.ok('framing', q) if ctx.art_has(r'unverified|unsubstantiated|not (?:proven|verified)|(?:none|no|without)[^.]{0,80}(?:logs|evidence)') else ctx.fail('framing', q, 'Mark allegations as unverified.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
