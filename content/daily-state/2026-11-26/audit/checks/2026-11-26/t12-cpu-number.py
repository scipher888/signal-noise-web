import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't12-cpu-number', 'artifact': 'takeaways', 'type': 'number', 'story': 'Messages API migration', 'quote': 'about 70 percent'}


def check(ctx):
    return ctx.require('anthropic', r'about 70% less CPU per request')


if __name__ == '__main__':
    run_cli(CLAIM, check)
