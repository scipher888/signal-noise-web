import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e36-66-interviews-58-customers', 'artifact': 'episode', 'type': 'number', 'story': 'Anthropic Enterprise Study', 'quote': '66 interviews across 58 of its own business customers'}


def check(ctx):
    return ctx.require('anthropic', r'66 interviews with 58 of Anthropic.s enterprise customers')


if __name__ == '__main__':
    run_cli(CLAIM, check)
