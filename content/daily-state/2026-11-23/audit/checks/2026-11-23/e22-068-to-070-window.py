import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e22-068-to-070-window', 'artifact': 'episode', 'type': 'number', 'story': 'OpenAI Perplexity', 'quote': 'the zero point six eight to zero point seven zero window'}


def check(ctx):
    return ctx.require('openai', r'~0\.68[-–]0\.70?\s+log-perplexity window')


if __name__ == '__main__':
    run_cli(CLAIM, check)
