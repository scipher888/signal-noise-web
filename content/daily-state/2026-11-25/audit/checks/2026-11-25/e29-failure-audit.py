import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e29-failure-audit', 'artifact': 'episode', 'type': 'attribution', 'story': "Humanity's First Exam", 'quote': 'The failure logs explain why'}


def check(ctx):
    return ctx.require('deepmind', r'paper.s audit of 58,752 rollouts.*5,552 wrong answers', r'Visual perception errors \(73% of wrong rollouts\)', note='Audit attributes errors to categories, not to a causal mechanism in training.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
