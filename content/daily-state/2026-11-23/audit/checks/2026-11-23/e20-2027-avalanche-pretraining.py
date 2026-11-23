import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e20-2027-avalanche-pretraining', 'artifact': 'episode', 'type': 'attribution', 'story': 'OpenAI Perplexity', 'quote': 'He warns that as soon as 2027, we could see an avalanche of AI-driven breakthroughs in pretraining research'}


def check(ctx):
    return ctx.require('openai', r'as soon as 2027.*avalanche of fundamental pretraining advancements')


if __name__ == '__main__':
    run_cli(CLAIM, check)
