import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e16-forty-eight-hours', 'artifact': 'episode', 'type': 'number', 'story': 'GitHub publishing', 'quote': 'what landed on GitHub in forty-eight hours'}


def check(ctx):
    return ctx.require('framing', r'(?=.*GitHub)(?=.*(?:48|forty-eight)[ -]hours?)(?=.*(?:posted|committed|uploaded))', note='A commit chronology is needed.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
