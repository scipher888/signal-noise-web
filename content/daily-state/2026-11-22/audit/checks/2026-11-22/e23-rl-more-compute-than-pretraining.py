import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e23-rl-more-compute-than-pretraining', 'artifact': 'episode', 'type': 'comparison', 'story': 'Nathan Lambert Cornell talk', 'quote': 'Reinforcement learning now consumes far more compute than pretraining'}


def check(ctx):
    return ctx.require('lambert', r'Post-training \(RL\) now takes most of a frontier lab.s compute', r'RL compute relative to pretraining compute')


if __name__ == '__main__':
    run_cli(CLAIM, check)
