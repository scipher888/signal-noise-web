import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e45-no-outage', 'artifact': 'episode', 'type': 'number', 'story': 'Rust migration', 'quote': 'with zero downtime'}


def check(ctx):
    return ctx.require('anthropic', r'ship an API on Rust.{0,150}without ever taking the service offline')


if __name__ == '__main__':
    run_cli(CLAIM, check)
