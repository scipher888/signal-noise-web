import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e58-common-bugs', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Production verification', 'quote': 'common bugs fired across huge waves of requests'}


def check(ctx):
    return ctx.require('anthropic', r'a single common bug can cause many mismatches', r'A single bug could produce hundreds of thousands of nearly identical diff records')


if __name__ == '__main__':
    run_cli(CLAIM, check)
