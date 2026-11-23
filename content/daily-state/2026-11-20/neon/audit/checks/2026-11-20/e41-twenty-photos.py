import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e41-twenty-photos', 'artifact': 'episode', 'type': 'number', 'story': 'Blueprint', 'quote': 'agents turn roughly twenty apartment photos into 2D floor plans'}


def check(ctx):
    return ctx.require('blueprint', r'~20 interior photos', r'2D floor plans')


if __name__ == '__main__':
    run_cli(CLAIM, check)
