import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's12-card-mega', 'artifact': 'short', 'type': 'comparison', 'story': 'Airbnb', 'quote': 'Fine-tuning beat mega-prompts'}


def check(ctx):
    return ctx.require('airbnb', r"Hundreds of thousands of in-domain examples did what a 2,700 word prompt couldn't")


if __name__ == '__main__':
    run_cli(CLAIM, check)
