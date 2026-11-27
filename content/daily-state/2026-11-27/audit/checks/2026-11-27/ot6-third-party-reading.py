import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot6-third-party-reading', 'artifact': 'takeaways', 'type': 'objection', 'story': 'Pretraining loss', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'Third-party analysis of company-reported OpenAI loss data')
    return ctx.ok('framing', q) if ctx.art_has(r'METR[^.!?]{0,100}(?:reading|analy[sz]|reported from|interpret)[^.!?]{0,60}OpenAI') else ctx.fail('framing', q, 'Identify METR’s secondary analysis.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
