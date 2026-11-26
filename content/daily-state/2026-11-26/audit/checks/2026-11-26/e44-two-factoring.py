import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e44-two-factoring', 'artifact': 'episode', 'type': 'number', 'story': 'Google factoring', 'quote': 'two new results on integer factoring'}


def check(ctx):
    return ctx.require('framing', r'(?=.*(?:two|2) new (?:results|papers))(?=.*integer factoring)', note='Six papers overall does not specify the factoring subtotal.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
