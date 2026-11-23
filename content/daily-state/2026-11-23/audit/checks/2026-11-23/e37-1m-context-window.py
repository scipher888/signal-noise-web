import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e37-1m-context-window', 'artifact': 'episode', 'type': 'number', 'story': 'Ant Group LingSante', 'quote': 'a one-million-token context window'}


def check(ctx):
    return ctx.require('lingsante', r'1-million-token context window')


if __name__ == '__main__':
    run_cli(CLAIM, check)
