import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot9-no-consensus', 'artifact': 'takeaways', 'type': 'objection', 'story': 'Pretraining loss', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'METR states it has no consensus view')
    return ctx.ok('framing', q) if ctx.art_has(r'no consensus|staff (?:disagreed|disagree|were divided)') else ctx.fail('framing', q, 'Include METR’s lack of consensus.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
