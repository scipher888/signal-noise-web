import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e28-e2b-rtx', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Airbnb', 'quote': 'a fine-tuned Gemma 4 E2B model on a single NVIDIA RTX Pro 6000 GPU'}


def check(ctx):
    return ctx.require('gemma', r'Gemma 4 E2B .*single @NVIDIA RTX Pro 6000 GPU')


if __name__ == '__main__':
    run_cli(CLAIM, check)
