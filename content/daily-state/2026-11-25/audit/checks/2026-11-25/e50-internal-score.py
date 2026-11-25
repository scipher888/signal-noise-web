import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e50-internal-score', 'artifact': 'episode', 'type': 'number', 'story': 'Protein design', 'quote': "OpenAI's latest internal model scores under 0.4 on a one-point scale"}


def check(ctx):
    return ctx.require('openai', r'average score rose from.*0\.38 for our latest internal model', r'A score of 1 means a perfect match to the real structure')


if __name__ == '__main__':
    run_cli(CLAIM, check)
