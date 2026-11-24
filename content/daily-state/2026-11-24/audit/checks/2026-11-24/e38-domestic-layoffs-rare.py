import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e38-domestic-layoffs-rare', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Anthropic Enterprise Study', 'quote': 'domestic layoffs are still rare'}


def check(ctx):
    return ctx.require('anthropic', r'very few examples of domestic layoffs')


if __name__ == '__main__':
    run_cli(CLAIM, check)
