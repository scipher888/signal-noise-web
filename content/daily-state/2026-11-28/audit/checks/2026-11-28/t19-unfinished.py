import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't19-unfinished', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Benchmarks and builder reports', 'quote': 'unfinished builds'}


def check(ctx):
    return ctx.require('thezvi', r'stopped too soon on end-to-end builds')


if __name__ == '__main__':
    run_cli(CLAIM, check)
