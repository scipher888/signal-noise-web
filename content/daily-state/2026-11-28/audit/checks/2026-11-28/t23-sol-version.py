import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't23-sol-version', 'artifact': 'takeaways', 'type': 'number', 'story': 'Benchmarks and builder reports', 'quote': 'Sol 6.2'}


def check(ctx):
    return ctx.require('thezvi', r'Kevin Lacker: Sol 6\.2 is the real winner of the 6\.2 series')


if __name__ == '__main__':
    run_cli(CLAIM, check)
