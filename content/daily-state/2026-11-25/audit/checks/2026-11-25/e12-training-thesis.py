import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e12-training-thesis', 'artifact': 'episode', 'type': 'opinion', 'story': 'Discovery vs. reliability', 'quote': 'Intense training on math and code has turned frontier models into remarkable discovery engines'}


def check(ctx):
    return ctx.need('gpt62', ctx.find('gpt62', r'My intuition suggests.*post-training regime'), 'Causal interpretation across models, not a controlled training result.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
