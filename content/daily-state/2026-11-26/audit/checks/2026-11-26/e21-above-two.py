import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e21-above-two', 'artifact': 'episode', 'type': 'number', 'story': 'Matrix multiplication', 'quote': 'a lower bound above two'}


def check(ctx):
    return ctx.require('framing', r'(?=.*matrix multiplication)(?=.*lower bound (?:strictly )?(?:above|greater than|exceeding) (?:2|two)\b)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
