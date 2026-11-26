import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e32-presumed-correct', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Aaronson on proofs', 'quote': 'correct unless shown otherwise'}


def check(ctx):
    return ctx.require('framing', r'(?=.*Aaronson)(?=.*proofs?)(?=.*correct until|.*correct unless)(?=.*(?:shown|demonstrated|proved) otherwise)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
