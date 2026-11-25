import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e67-unsigned', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Chabot sketchbook', 'quote': 'the diary was unsigned'}


def check(ctx):
    return ctx.require('gpt62', r'because the diary was not signed')


if __name__ == '__main__':
    run_cli(CLAIM, check)
