import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't10-migration-direction', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Messages API migration', 'quote': 'migrating its Messages API from Python to Rust'}


def check(ctx):
    return ctx.require('anthropic', r'we migrated our Messages API from Python to Rust')


if __name__ == '__main__':
    run_cli(CLAIM, check)
