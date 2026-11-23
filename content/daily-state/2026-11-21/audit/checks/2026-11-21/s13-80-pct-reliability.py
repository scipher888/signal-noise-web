import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's13-80-pct-reliability', 'artifact': 'short', 'type': 'number', 'story': 'AI Autonomous Horizons', 'quote': 'At eighty percent reliability'}


def check(ctx):
    return ctx.require('naam', r'80% successful.*nine minutes at Google')


if __name__ == '__main__':
    run_cli(CLAIM, check)
