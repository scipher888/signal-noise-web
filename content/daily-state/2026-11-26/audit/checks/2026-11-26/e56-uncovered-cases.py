import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e56-uncovered-cases', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Production verification', 'quote': 'Real traffic hit uncovered edge cases'}


def check(ctx):
    return ctx.require('anthropic', r'cases in production traffic that our tests didn.t cover')


if __name__ == '__main__':
    run_cli(CLAIM, check)
