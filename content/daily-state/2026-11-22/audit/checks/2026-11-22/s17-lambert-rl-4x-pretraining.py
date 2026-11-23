import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's17-lambert-rl-4x-pretraining', 'artifact': 'short', 'type': 'attribution', 'story': 'AI Verification & Riemann Proof', 'quote': 'Nathan Lambert notes RL now takes up to four times more compute than pretraining'}


def check(ctx):
    return ctx.require('lambert', r'RL compute relative to pretraining compute', r'~4×')


if __name__ == '__main__':
    run_cli(CLAIM, check)
