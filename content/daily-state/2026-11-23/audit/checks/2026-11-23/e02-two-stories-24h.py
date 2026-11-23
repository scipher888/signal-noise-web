import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e02-two-stories-24h', 'artifact': 'episode', 'type': 'number', 'story': 'Overview', 'quote': 'Two big stories landed in AI over the past twenty-four hours'}


def check(ctx):
    return ctx.need(None, None, 'Editorial count and 24-hour timing relative to broadcast date cannot be verified from source text alone')


if __name__ == '__main__':
    run_cli(CLAIM, check)
