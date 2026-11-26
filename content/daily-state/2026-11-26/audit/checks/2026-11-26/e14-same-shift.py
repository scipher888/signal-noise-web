import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e14-same-shift', 'artifact': 'episode', 'type': 'opinion', 'story': 'Dual-use mathematics', 'quote': 'They are actually two halves of the same shift'}


def check(ctx):
    return ctx.need(None, None, 'Interpretation, not a reported finding.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
