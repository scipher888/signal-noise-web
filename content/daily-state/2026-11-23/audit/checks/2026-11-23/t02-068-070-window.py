import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't02-068-070-window', 'artifact': 'takeaways', 'type': 'number', 'story': 'OpenAI perplexity warning', 'quote': '0.68 to 0.70 log-perplexity window'}


def check(ctx):
    return ctx.require('openai', r'~0\.68[-–]0\.70?\s+log-perplexity window')


if __name__ == '__main__':
    run_cli(CLAIM, check)
