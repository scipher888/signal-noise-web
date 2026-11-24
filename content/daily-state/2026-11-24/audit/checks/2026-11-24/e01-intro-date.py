import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e01-intro-date', 'artifact': 'episode', 'type': 'number', 'story': 'Intro', 'quote': 'Tuesday, November 24, 2026'}


def check(ctx):
    return ctx.need(None, None, 'Episode date Tuesday, November 24, 2026 is not stated in source texts (primary articles are dated Nov 23, 2026)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
