import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot3-partner-lab', 'artifact': 'takeaways', 'type': 'objection', 'story': 'GPT-6 protein binders', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'lab tests run by its research partner Onava')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:lab|research) partner[, :]+Onava|Onava.{0,40}(?:partner|ran the lab tests)') else ctx.fail('framing', q, 'Identify Onava as the partner lab.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
