import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e01-episode-date', 'artifact': 'episode', 'type': 'number', 'story': 'Daily State of AI', 'quote': 'Friday, November 27th, 2026'}


def check(ctx):
    return ctx.require('framing', r'Friday,? November 27(?:th)?,? 2026', note='Check the episode dateline, not the date of either news story.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
