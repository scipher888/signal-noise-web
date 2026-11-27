import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't04-rate', 'artifact': 'takeaways', 'type': 'number', 'story': 'Pretraining loss', 'quote': 'roughly seven times faster'}


def check(ctx):
    return ctx.require('metr', r'pretraining loss: since early 2026, it has been falling about seven times faster')


if __name__ == '__main__':
    run_cli(CLAIM, check)
