import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e09-conditional', 'artifact': 'episode', 'type': 'qualifier', 'story': 'OpenAI loss curve', 'quote': 'If that pace holds'}


def check(ctx):
    return ctx.require('metr', r'If the current pace holds, OpenAI would cover the drop')


if __name__ == '__main__':
    run_cli(CLAIM, check)
