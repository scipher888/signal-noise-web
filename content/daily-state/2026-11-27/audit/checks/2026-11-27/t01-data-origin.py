import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't01-data-origin', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Pretraining loss', 'quote': "METR reported from OpenAI's published data"}


def check(ctx):
    return ctx.require('metr', r'author = \{METR\}', r'OpenAI recently published the base-model log-perplexity of 13 models')


if __name__ == '__main__':
    run_cli(CLAIM, check)
