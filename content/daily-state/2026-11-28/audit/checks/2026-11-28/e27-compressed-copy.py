import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e27-compressed-copy', 'artifact': 'episode', 'type': 'number', 'story': 'Mir2k', 'quote': 'one upload compressed the binary to wipe out standard file signatures'}


def check(ctx):
    return ctx.require('gguf', r'Its second model carries the same program compressed.*removes every recognizable file signature')


if __name__ == '__main__':
    run_cli(CLAIM, check)
