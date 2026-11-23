import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e36-rpm', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Airbnb', 'quote': 'only beats APIs above fifteen to thirty requests per minute'}


def check(ctx):
    return ctx.require('airbnb', r'below roughly 15 to 30 RPM, Claude Sonnet 5\.5 and GPT-6\.1 Sol are cheaper')


if __name__ == '__main__':
    run_cli(CLAIM, check)
