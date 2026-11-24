import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e39-two-thirds-hiring-less', 'artifact': 'episode', 'type': 'number', 'story': 'Anthropic Enterprise Study', 'quote': 'two-thirds of these companies say they are hiring less because of AI'}


def check(ctx):
    return ctx.require('anthropic', r'two-thirds of the companies we spoke to reported reduced hiring due to AI')


if __name__ == '__main__':
    run_cli(CLAIM, check)
