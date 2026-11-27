import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't02-full-comparison', 'artifact': 'takeaways', 'type': 'comparison', 'story': 'Pretraining loss', 'quote': 'base-model pretraining loss on an internal codebase slice has fallen roughly seven times faster since early 2026 than in 2022 through 2025'}


def check(ctx):
    return ctx.require('metr', r'base-model log-perplexity.*fixed held-out dataset sourced from its own codebase', r'pretraining loss: since early 2026, it has been falling about seven times faster than it was from 2022 through 2025')


if __name__ == '__main__':
    run_cli(CLAIM, check)
