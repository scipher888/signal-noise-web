import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e39-dial', 'artifact': 'episode', 'type': 'opinion', 'story': 'Airbnb', 'quote': "You can't prompt your way to an operational dial"}


def check(ctx):
    s = ctx.find('airbnb', r'Scores let you choose your tradeoff .* without rewriting the prompt')
    return ctx.need('airbnb', s, 'opinion; paraphrases the quoted source line')


if __name__ == '__main__':
    run_cli(CLAIM, check)
