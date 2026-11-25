import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e10-coverage', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Discovery vs. reliability', 'quote': 'a divide most coverage misses'}


def check(ctx):
    return ctx.need('kaggle', ctx.find('kaggle', r'That disconnect is called jagged intelligence'), 'No survey of coverage establishes how often this distinction is missed.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
