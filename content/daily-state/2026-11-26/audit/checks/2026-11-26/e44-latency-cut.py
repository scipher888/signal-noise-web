import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e44-latency-cut', 'artifact': 'episode', 'type': 'number', 'story': 'Rust migration', 'quote': 'median time to first token by about twenty percent'}


def check(ctx):
    return ctx.require('anthropic', r'cuts median time to first token by about 20%')


if __name__ == '__main__':
    run_cli(CLAIM, check)
