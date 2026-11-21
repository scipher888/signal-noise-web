import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's14-robotics-zero', 'artifact': 'short', 'type': 'attribution', 'story': 'Blueprint', 'quote': 'a dedicated robotics model scored zero'}


def check(ctx):
    return ctx.require('blueprint', r'Gemini Robotics-ER 1\.6 0\.000\*\*')


if __name__ == '__main__':
    run_cli(CLAIM, check)
