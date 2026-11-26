import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e21-rumor-duration', 'artifact': 'episode', 'type': 'number', 'story': 'Factoring rumor', 'quote': 'unverified ten-day rumor'}


def check(ctx):
    return ctx.require('andrewcurran_', r'this rumor has persisted for about ten days, about both Anthropic and OpenAI', note='Approximate age of the rumor, not a confirmed discovery.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
