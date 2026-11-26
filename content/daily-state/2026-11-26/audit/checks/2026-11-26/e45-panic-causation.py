import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e45-panic-causation', 'artifact': 'episode', 'type': 'attribution', 'story': 'RSA rumors', 'quote': 'Those factoring papers immediately fueled the online panic'}


def check(ctx):
    return ctx.require('kimmonismus', r'(?=.*Google)(?=.*factoring papers)(?=.*(?:immediately|as soon as))(?=.*(?:sparked|fueled|triggered).*(?:panic|rumors))', note='Temporal proximity and speculation about other labs are not causation.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
