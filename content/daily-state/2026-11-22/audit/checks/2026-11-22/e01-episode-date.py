import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e01-episode-date', 'artifact': 'episode', 'type': 'number', 'story': 'Daily State of AI', 'quote': 'Sunday, November 22, 2026'}


def check(ctx):
    q = ctx.find('lean', r'2026-11-21')
    return ctx.need('lean', q, 'Broadcast date Sunday, November 22, 2026 is not stated in primary sources (dated Nov 20-21, 2026)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
