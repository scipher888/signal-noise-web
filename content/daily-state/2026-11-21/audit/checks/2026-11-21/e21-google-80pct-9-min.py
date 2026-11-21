import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e21-google-80pct-9-min', 'artifact': 'episode', 'type': 'number', 'story': 'AI task-horizon analysis', 'quote': 'Inside Google, at an eighty percent success rate, the real number is nine minutes.'}


def check(ctx):
    return ctx.require('naam', r'80% successful.*nine minutes at Google')


if __name__ == '__main__':
    run_cli(CLAIM, check)
