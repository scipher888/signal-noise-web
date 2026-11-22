import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e05-metr-capability-update', 'artifact': 'episode', 'type': 'attribution', 'story': 'METR capability update', 'quote': 'METR dropped a major capability update'}


def check(ctx):
    return ctx.require('metr', r'November 20, 2026', r'capability evaluations of public models')


if __name__ == '__main__':
    run_cli(CLAIM, check)
