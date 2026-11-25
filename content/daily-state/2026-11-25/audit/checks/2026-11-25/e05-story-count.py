import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e05-story-count', 'artifact': 'episode', 'type': 'number', 'story': 'Discovery vs. reliability', 'quote': "today's three biggest AI stories"}


def check(ctx):
    return ctx.require('framing', r'STORY: OpenAI says', r'STORY: A historian says', r'STORY: Google DeepMind', note='Checks the three distinct selected stories only; importance is a separate judgment.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
