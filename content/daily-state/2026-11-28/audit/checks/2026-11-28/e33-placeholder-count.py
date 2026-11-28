import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e33-placeholder-count', 'artifact': 'episode', 'type': 'number', 'story': 'Mir2k', 'quote': 'twelve empty placeholder repositories'}


def check(ctx):
    return ctx.require('gguf', r'Twelve of them are empty placeholders named after expected releases')


if __name__ == '__main__':
    run_cli(CLAIM, check)
