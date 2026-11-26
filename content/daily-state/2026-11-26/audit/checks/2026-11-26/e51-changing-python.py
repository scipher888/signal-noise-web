import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e51-changing-python', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Rust migration', 'quote': 'The Python service kept changing throughout the rewrite'}


def check(ctx):
    return ctx.require('anthropic', r'the Python API continued changing throughout the migration')


if __name__ == '__main__':
    run_cli(CLAIM, check)
