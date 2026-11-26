import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e43-cpu-cut', 'artifact': 'episode', 'type': 'number', 'story': 'Rust migration', 'quote': 'cut CPU use per request by about seventy percent'}


def check(ctx):
    return ctx.require('anthropic', r'uses about 70% less CPU per request')


if __name__ == '__main__':
    run_cli(CLAIM, check)
