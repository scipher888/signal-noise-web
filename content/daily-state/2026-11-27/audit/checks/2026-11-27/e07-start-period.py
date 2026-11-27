import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e07-start-period', 'artifact': 'episode', 'type': 'number', 'story': 'OpenAI loss curve', 'quote': 'Since early 2026'}


def check(ctx):
    return ctx.require('metr', r'pretraining loss: since early 2026, it has been falling')


if __name__ == '__main__':
    run_cli(CLAIM, check)
