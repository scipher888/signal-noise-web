import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e41-overhead', 'artifact': 'episode', 'type': 'comparison', 'story': 'Rust migration', 'quote': 'Anthropic needed far less overhead'}


def check(ctx):
    return ctx.require('anthropic', r'Python added overhead to every one of those steps', r'needed to find a way to make the service much more efficient', r'Rust would allow us to use far less CPU per request')


if __name__ == '__main__':
    run_cli(CLAIM, check)
