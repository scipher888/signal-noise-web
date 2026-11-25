import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e37-generation-only', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Protein design', 'quote': 'without calling specialized biology models during generation'}


def check(ctx):
    return ctx.require('openai', r'without calling specialized biology models to generate those designs')


if __name__ == '__main__':
    run_cli(CLAIM, check)
