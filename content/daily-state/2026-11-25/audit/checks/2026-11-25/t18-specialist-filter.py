import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't18-specialist-filter', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'GPT-6 protein binders', 'quote': 'specialized biology models still filtered weak candidates upfront'}


def check(ctx):
    return ctx.require('openai', r'protein design campaign relied on specialized structure prediction models.*to filter candidates', r'Specialized models supplied amino acid sequences and helped select candidates for testing')


if __name__ == '__main__':
    run_cli(CLAIM, check)
