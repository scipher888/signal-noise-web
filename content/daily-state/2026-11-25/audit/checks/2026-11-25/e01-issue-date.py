import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e01-issue-date', 'artifact': 'episode', 'type': 'number', 'story': 'Daily State of AI', 'quote': 'the Daily State of AI for Wednesday, November 25th, 2026'}


def check(ctx):
    return ctx.require('framing', r'(?:Daily State of AI|daily-state).*?(?:Wednesday, November 25(?:th)?, 2026|2026-11-25)', note='Check the issue date, not a research publication date.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
