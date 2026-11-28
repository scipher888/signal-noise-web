import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e29-nine-hours', 'artifact': 'episode', 'type': 'number', 'story': 'Mir2k', 'quote': 'twice in nine hours'}


def check(ctx):
    return ctx.require('gguf', r'both templates were replaced within about an hour', r'Nine hours later both were replaced again')


if __name__ == '__main__':
    run_cli(CLAIM, check)
