import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e15-template-count', 'artifact': 'episode', 'type': 'number', 'story': 'GGUF scan', 'quote': 'over five hundred and seventy thousand chat templates'}


def check(ctx):
    return ctx.require('gguf', r'parsed 572184 chat templates statically')


if __name__ == '__main__':
    run_cli(CLAIM, check)
