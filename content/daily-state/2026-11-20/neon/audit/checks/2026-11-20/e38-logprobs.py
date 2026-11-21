import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e38-logprobs', 'artifact': 'episode', 'type': 'attribution', 'story': 'Airbnb', 'quote': 'Extracting logprobs from a fine-tuned model gives Airbnb a continuous score they can threshold'}


def check(ctx):
    return ctx.require('airbnb', r'By extracting logprobs, we.re able to produce a score for thresholding')


if __name__ == '__main__':
    run_cli(CLAIM, check)
