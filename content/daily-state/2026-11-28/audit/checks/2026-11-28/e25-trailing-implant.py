import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e25-trailing-implant', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Mir2k', 'quote': 'ollie appended after the final model tensor'}


def check(ctx):
    return ctx.require('gguf', r'Windows remote access trojan named ollie hidden at the end of each file', r'executable already appended after its last tensor')


if __name__ == '__main__':
    run_cli(CLAIM, check)
