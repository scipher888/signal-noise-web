import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e46-discovery-game', 'artifact': 'episode', 'type': 'opinion', 'story': 'Protein design', 'quote': 'protein design is a discovery game'}


def check(ctx):
    return ctx.need('openai', ctx.find('openai', r'We can design far more proteins on a computer than we can make and test'), 'Editorial analogy.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
