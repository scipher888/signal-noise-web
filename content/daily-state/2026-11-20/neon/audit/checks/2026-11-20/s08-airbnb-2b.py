import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's08-airbnb-2b', 'artifact': 'short', 'type': 'attribution', 'story': 'Airbnb', 'quote': 'Airbnb fine-tuned a tiny 2-billion-parameter Gemma model'}


def check(ctx):
    return ctx.require('airbnb', r'fine-tuned classifier with 2 billion effective parameters', r'Fine-tuning Gemma4-E2B')


if __name__ == '__main__':
    run_cli(CLAIM, check)
