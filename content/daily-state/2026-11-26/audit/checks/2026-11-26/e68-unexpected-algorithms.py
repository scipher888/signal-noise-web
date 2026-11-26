import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e68-unexpected-algorithms', 'artifact': 'episode', 'type': 'attribution', 'story': 'Dual-use mathematics', 'quote': 'It also uncovers unexpected algorithms for what they can'}


def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'the running-time bound is subexponential'), 'A claimed bound does not establish unexpectedness or a general discovery process.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
