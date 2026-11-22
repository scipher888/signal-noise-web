import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's18-up-to-4x-compute-pretraining', 'artifact': 'short', 'type': 'comparison', 'story': 'AI Verification & Riemann Proof', 'quote': 'up to four times more compute than pretraining'}


def check(ctx):
    return ctx.require('lambert', r'RL compute relative to pretraining compute', r'~4×')


if __name__ == '__main__':
    run_cli(CLAIM, check)
