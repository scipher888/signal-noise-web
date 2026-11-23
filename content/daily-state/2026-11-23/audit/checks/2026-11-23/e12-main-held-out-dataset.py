import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e12-main-held-out-dataset', 'artifact': 'episode', 'type': 'qualifier', 'story': 'OpenAI Perplexity', 'quote': "On OpenAI's main held-out evaluation dataset"}


def check(ctx):
    return ctx.require('openai', r'held-out dataset', r'main evaluation dataset')


if __name__ == '__main__':
    run_cli(CLAIM, check)
