import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't13-alleged-sabotage', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Claude refusal behavior', 'quote': 'claims that Claude sabotages machine-learning research'}


def check(ctx):
    return ctx.require('realastropulse', r'After seeing the .Claude sabotages your ML research. posts', note='Evidence of allegations, not evidence of sabotage.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
