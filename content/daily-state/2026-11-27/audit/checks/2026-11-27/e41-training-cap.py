import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e41-training-cap', 'artifact': 'episode', 'type': 'attribution', 'story': 'Anthropic capability limits', 'quote': 'during training, it capped capabilities that could most directly speed up frontier AI development'}


def check(ctx):
    return ctx.require('claude', r'During training, Anthropic says, it .took steps to limit advances in the specific research capabilities that could most directly accelerate AI development')


if __name__ == '__main__':
    run_cli(CLAIM, check)
