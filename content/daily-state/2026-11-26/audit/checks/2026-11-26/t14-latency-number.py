import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't14-latency-number', 'artifact': 'takeaways', 'type': 'number', 'story': 'Messages API migration', 'quote': 'about 20 percent'}


def check(ctx):
    return ctx.require('anthropic', r'cuts median time to first token by about 20%')


if __name__ == '__main__':
    run_cli(CLAIM, check)
