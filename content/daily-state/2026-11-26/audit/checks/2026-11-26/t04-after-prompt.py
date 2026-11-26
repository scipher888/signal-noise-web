import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't04-after-prompt', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Gemini math papers', 'quote': 'after the first prompt'}


def check(ctx):
    return ctx.require('google', r'no human interaction other than the initial prompt for Cogentic to\s+generate a full proof and formalization', note='Timing qualifier supported for the log-rank paper only.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
