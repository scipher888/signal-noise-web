import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e06-story-ranking', 'artifact': 'episode', 'type': 'opinion', 'story': 'Discovery vs. reliability', 'quote': "today's three biggest AI stories"}


def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'STORY: Google DeepMind'), 'Selection is documented; biggest is an editorial ranking.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
