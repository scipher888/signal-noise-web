import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e47-robotics-zero', 'artifact': 'episode', 'type': 'number', 'story': 'Blueprint', 'quote': 'Gemini Robotics-ER 1.6, a model built specifically for embodied spatial reasoning, scored zero'}


def check(ctx):
    return ctx.require('blueprint', r'Gemini Robotics-ER 1\.6 0\.000\*\*', r'designed for spatial and embodied reasoning')


if __name__ == '__main__':
    run_cli(CLAIM, check)
