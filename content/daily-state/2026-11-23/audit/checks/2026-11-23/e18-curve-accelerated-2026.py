import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e18-curve-accelerated-2026', 'artifact': 'episode', 'type': 'number', 'story': 'OpenAI Perplexity', 'quote': "OpenAI's curve accelerated sharply in 2026"}


def check(ctx):
    return ctx.require('openai', r'steep acceleration in 2026')


if __name__ == '__main__':
    run_cli(CLAIM, check)
