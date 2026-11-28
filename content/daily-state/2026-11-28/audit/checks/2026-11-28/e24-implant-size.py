import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e24-implant-size', 'artifact': 'episode', 'type': 'number', 'story': 'Mir2k', 'quote': 'an eleven-and-a-half-megabyte Windows remote access trojan called ollie'}


def check(ctx):
    return ctx.require('gguf', r'same 11\.47 MB Windows x64 program', r'Windows remote access trojan named ollie', note='11.47 MB rounds to 11.5 MB.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
