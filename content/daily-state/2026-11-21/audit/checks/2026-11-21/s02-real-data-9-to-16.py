import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's02-real-data-9-to-16', 'artifact': 'short', 'type': 'attribution', 'story': 'AI Autonomous Horizons', 'quote': 'real data from Google and OpenAI shows AI only works autonomously for nine to sixteen minutes'}


def check(ctx):
    return ctx.require('naam', r'nine minutes at Google and an adjusted 16 minutes at OpenAI')


if __name__ == '__main__':
    run_cli(CLAIM, check)
