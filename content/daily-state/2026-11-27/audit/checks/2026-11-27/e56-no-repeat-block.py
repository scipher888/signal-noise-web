import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e56-no-repeat-block', 'artifact': 'episode', 'type': 'qualifier', 'story': 'API refusal and fallback behavior', 'quote': 'without repeating the fallback block'}


def check(ctx):
    return ctx.require('framing', r'(?:without repeating|do not repeat|omit).*fallback (?:block|notice)', note='Need the API description of subsequent turns.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
