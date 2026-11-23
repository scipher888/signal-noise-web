import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e14-gpt4-091', 'artifact': 'episode', 'type': 'number', 'story': 'OpenAI Perplexity', 'quote': 'GPT-4 hit about zero point nine one'}


def check(ctx):
    return ctx.require('openai', r'GPT.?4.*~0\.91')


if __name__ == '__main__':
    run_cli(CLAIM, check)
