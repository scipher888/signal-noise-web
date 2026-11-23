import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e13-gpt35-099', 'artifact': 'episode', 'type': 'number', 'story': 'OpenAI Perplexity', 'quote': 'GPT-3.5 sat around zero point nine nine'}


def check(ctx):
    return ctx.require('openai', r'GPT.?3\.5.*~0\.99')


if __name__ == '__main__':
    run_cli(CLAIM, check)
