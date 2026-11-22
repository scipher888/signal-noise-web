import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't07-claude-assisted', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Riemann Hypothesis Lean proof', 'quote': 'Claude-assisted'}


def check(ctx):
    q = ctx.find('lean', r'Claude')
    if q:
        return ctx.ok('lean', q)
    return ctx.need('lean', None, 'Primary source lean does not mention Claude')


if __name__ == '__main__':
    run_cli(CLAIM, check)
