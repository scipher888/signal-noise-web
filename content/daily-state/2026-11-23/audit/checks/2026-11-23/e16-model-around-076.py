import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e16-model-around-076', 'artifact': 'episode', 'type': 'number', 'story': 'OpenAI Perplexity', 'quote': 'a model around zero point seven six'}


def check(ctx):
    return ctx.require('openai', r'model of log-perplexity ~0\.76')


if __name__ == '__main__':
    run_cli(CLAIM, check)
