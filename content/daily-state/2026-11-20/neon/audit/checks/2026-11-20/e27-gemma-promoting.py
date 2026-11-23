import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e27-gemma-promoting', 'artifact': 'episode', 'type': 'attribution', 'story': 'Airbnb', 'quote': "Google's Gemma account is promoting Airbnb's new benchmark"}


def check(ctx):
    return ctx.require('gemma', r'@googlegemma: Love seeing what happens when open weights meet great engineering')


if __name__ == '__main__':
    run_cli(CLAIM, check)
