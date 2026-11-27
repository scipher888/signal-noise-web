import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e08-loss-rate', 'artifact': 'episode', 'type': 'comparison', 'story': 'OpenAI loss curve', 'quote': 'loss has fallen roughly seven times faster than it did from 2022 through 2025'}


def check(ctx):
    return ctx.require('metr', r'pretraining loss: since early 2026, it has been falling about seven times faster than it was from 2022 through 2025')


if __name__ == '__main__':
    run_cli(CLAIM, check)
