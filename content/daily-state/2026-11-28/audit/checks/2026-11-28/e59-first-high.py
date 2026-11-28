import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e59-first-high', 'artifact': 'episode', 'type': 'comparison', 'story': 'Astra risk rating', 'quote': "OpenAI's first external release rated High for accelerating AI research"}


def check(ctx):
    return ctx.require('gpt', r'Astra is our first externally released model to meet the High threshold for AI Self-improvement.*accelerate AI research')


if __name__ == '__main__':
    run_cli(CLAIM, check)
