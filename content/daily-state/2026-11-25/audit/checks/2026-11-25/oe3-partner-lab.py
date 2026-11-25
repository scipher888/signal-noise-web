import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe3-partner-lab', 'artifact': 'episode', 'type': 'objection', 'story': 'Protein design', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'lab tests run by its research partner Onava')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:lab|research) partner[, :]+Onava|Onava.{0,40}(?:partner|ran the lab tests)') else ctx.fail('framing', q, 'Name Onava as the partner conducting lab tests.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
