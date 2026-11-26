import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't13-joint-comparison', 'artifact': 'takeaways', 'type': 'comparison', 'story': 'Messages API migration', 'quote': 'cut CPU use per request by about 70 percent and median time to first token by about 20 percent'}


def check(ctx):
    return ctx.require('anthropic', r'uses about 70% less CPU per request and cuts median time to first token by about 20%')


if __name__ == '__main__':
    run_cli(CLAIM, check)
