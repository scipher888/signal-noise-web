import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe8-third-party-reading', 'artifact': 'episode', 'type': 'objection', 'story': 'METR chart debate', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'Third-party analysis of company-reported OpenAI loss data')
    return ctx.ok('framing', q) if ctx.art_has(r'METR[^.!?]{0,100}(?:reading|analy[sz]|reported from|graph out of|interpret)[^.!?]{0,60}OpenAI|METR.s (?:analysis|reading) of OpenAI') else ctx.fail('framing', q, 'Distinguish METR’s reading from a new independent measurement.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
