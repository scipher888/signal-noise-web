import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e16-metr-agent-swarms', 'artifact': 'episode', 'type': 'attribution', 'story': 'METR capability update', 'quote': 'METR ran experiments with agent swarms'}


def check(ctx):
    return ctx.require('metr', r'ran small experiments with swarms')


if __name__ == '__main__':
    run_cli(CLAIM, check)
