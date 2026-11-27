import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e44-ordinary-ml', 'artifact': 'episode', 'type': 'attribution', 'story': 'Anthropic capability limits', 'quote': 'Anthropic says traditional machine-learning work is untouched'}


def check(ctx):
    return ctx.require('claude', r'Anthropic.s November disclosure explicitly carves out traditional AI and machine learning research')


if __name__ == '__main__':
    run_cli(CLAIM, check)
