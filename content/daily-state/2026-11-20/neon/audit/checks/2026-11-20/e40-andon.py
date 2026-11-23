import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e40-andon', 'artifact': 'episode', 'type': 'attribution', 'story': 'Blueprint', 'quote': "Andon Labs' Blueprint-Bench 2"}


def check(ctx):
    return ctx.require('blueprint', r'author=\{Andon Labs\}')


if __name__ == '__main__':
    run_cli(CLAIM, check)
