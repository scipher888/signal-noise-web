import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e26-leader', 'artifact': 'episode', 'type': 'number', 'story': "Humanity's First Exam", 'quote': "OpenAI's GPT-6.2 Astra leads Kaggle's initial run near 91 percent"}


def check(ctx):
    return ctx.require('kaggle', r'Current leaderboard:', r'🥇\s*GPT-\s*6\.2 Astra \(xhigh\) - 90\.7%')


if __name__ == '__main__':
    run_cli(CLAIM, check)
