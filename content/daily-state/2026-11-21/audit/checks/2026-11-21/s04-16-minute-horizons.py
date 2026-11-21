import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's04-16-minute-horizons', 'artifact': 'short', 'type': 'number', 'story': 'AI Autonomous Horizons', 'quote': '16-Minute Horizons'}


def check(ctx):
    return ctx.require('naam', r'16 minutes at OpenAI')


if __name__ == '__main__':
    run_cli(CLAIM, check)
