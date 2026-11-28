import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't18-every-criticism', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Benchmarks and builder reports', 'quote': 'Every criticizes its writing and unfinished builds'}


def check(ctx):
    return ctx.require('thezvi', r'Every: No one on our team loved Astra 6\.2', r'Astra 6\.2 is a real step back for writing', r'for coding we found it stopped too soon on end-to-end builds')


if __name__ == '__main__':
    run_cli(CLAIM, check)
