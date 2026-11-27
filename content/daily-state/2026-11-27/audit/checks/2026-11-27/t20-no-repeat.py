import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't20-no-repeat', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Claude refusal behavior', 'quote': 'without repeating the fallback notice'}


def check(ctx):
    return ctx.require('framing', r'(?:without repeating|omit|do not repeat).*fallback (?:block|notice)', note='Verify subsequent response format in actual documentation.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
