import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't03-roughly-qualifier', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'METR AI agent time horizon', 'quote': 'roughly'}


def check(ctx):
    return ctx.require('metr', r'very roughly equivalent to halving')


if __name__ == '__main__':
    run_cli(CLAIM, check)
