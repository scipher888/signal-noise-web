import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e39-gemini-base', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Google papers', 'quote': 'running on Gemini 4'}


def check(ctx):
    return ctx.require('google', r'using Gemini 4 as the base model')


if __name__ == '__main__':
    run_cli(CLAIM, check)
