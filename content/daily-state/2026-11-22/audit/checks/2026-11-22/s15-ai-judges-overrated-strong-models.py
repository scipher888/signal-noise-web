import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's15-ai-judges-overrated-strong-models', 'artifact': 'short', 'type': 'comparison', 'story': 'AI Verification & Riemann Proof', 'quote': 'AI judges systematically overrated strong models'}


def check(ctx):
    return ctx.require('metr', r'systematically overestimate the quality of their own solutions, and those of stronger models')


if __name__ == '__main__':
    run_cli(CLAIM, check)
