import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e01-edition-date', 'artifact': 'episode', 'type': 'number', 'story': 'Edition date', 'quote': 'Daily State of AI for Thursday, November 26th, 2026'}


def check(ctx):
    return ctx.require('framing', r'Thursday,?\s+(?:November 26(?:th)?,? 2026|26 November 2026)', note='A dated URL is not an edition dateline.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
