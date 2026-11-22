import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e20-opus-overrated-astra-tasks', 'artifact': 'episode', 'type': 'attribution', 'story': 'METR capability update', 'quote': 'When METR asked Opus 5.5 to grade evaluation tasks designed by GPT-6 Astra, it systematically overrated them'}


def check(ctx):
    return ctx.require('metr', r'Opus 5\.5.*scores Astra.s tasks on average about 0\.2.*more highly than our human', r'systematically overestimate')


if __name__ == '__main__':
    run_cli(CLAIM, check)
