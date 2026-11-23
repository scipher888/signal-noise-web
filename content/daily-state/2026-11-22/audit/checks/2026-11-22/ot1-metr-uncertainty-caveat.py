import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot1-metr-uncertainty-caveat', 'artifact': 'takeaways', 'type': 'objection', 'story': 'METR AI agent time horizon', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'evaluator-reported research update with wide uncertainty, not independent replication')
    if not ctx.art_has(r'uncertain|confidence interval|not independent|independent replication|self-reported|own evaluation|evaluator-reported'):
        return ctx.fail('framing', q, 'Takeaways omit METR framing caveat: evaluator-reported update with wide uncertainty, not independent replication')
    return ctx.ok('framing', q)


if __name__ == '__main__':
    run_cli(CLAIM, check)
