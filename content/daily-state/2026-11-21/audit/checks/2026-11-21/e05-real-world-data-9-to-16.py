import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e05-real-world-data-9-to-16', 'artifact': 'episode', 'type': 'attribution', 'story': 'AI task-horizon analysis', 'quote': 'a major new analysis of real-world data from inside OpenAI and Google shows AI can only work autonomously for nine to sixteen minutes before falling short'}


def check(ctx):
    return ctx.require('naam', r'nine minutes at Google and an adjusted 16 minutes at OpenAI')


if __name__ == '__main__':
    run_cli(CLAIM, check)
