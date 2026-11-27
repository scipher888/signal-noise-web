import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e04-openai-publication', 'artifact': 'episode', 'type': 'attribution', 'story': 'OpenAI loss curve', 'quote': 'OpenAI recently published base-model pretraining loss'}


def check(ctx):
    return ctx.require('metr', r'OpenAI recently published the base-model log-perplexity')


if __name__ == '__main__':
    run_cli(CLAIM, check)
