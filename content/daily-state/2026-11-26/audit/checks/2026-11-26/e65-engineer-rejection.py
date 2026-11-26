import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e65-engineer-rejection', 'artifact': 'episode', 'type': 'attribution', 'story': 'Shadow oracle', 'quote': 'An engineer had to reject it as throwaway code'}


def check(ctx):
    return ctx.require('anthropic', r'propose a fix, which an engineer rejects as throwaway code')


if __name__ == '__main__':
    run_cli(CLAIM, check)
