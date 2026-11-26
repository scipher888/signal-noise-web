import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e72-holiday', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Broadcast', 'quote': 'have a great Thanksgiving'}


def check(ctx):
    return ctx.need(None, None, 'Sign-off; no broadcast calendar in the source texts.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
