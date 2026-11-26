import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't19-week', 'artifact': 'takeaways', 'type': 'number', 'story': 'Messages API migration', 'quote': 'in about a week'}


def check(ctx):
    return ctx.require('anthropic', r'Claude wrote a first version of the API.s core request path in about a week')


if __name__ == '__main__':
    run_cli(CLAIM, check)
