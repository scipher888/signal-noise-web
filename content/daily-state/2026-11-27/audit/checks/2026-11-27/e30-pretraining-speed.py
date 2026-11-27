import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e30-pretraining-speed', 'artifact': 'episode', 'type': 'comparison', 'story': 'Sources of acceleration', 'quote': 'Pretraining is moving faster'}


def check(ctx):
    return ctx.require('metr', r'acceleration in pretraining loss: since early 2026, it has been falling about seven times faster', note='Supports faster progress in measured loss, not shorter training runtimes.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
