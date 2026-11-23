import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's04-metr-horizons-doubling-3-6', 'artifact': 'short', 'type': 'attribution', 'story': 'AI Verification & Riemann Proof', 'quote': 'METR showed AI task horizons doubling every 3.6 months'}


def check(ctx):
    return ctx.require('metr', r'time horizons are doubling roughly every 3\.6\d* months')


if __name__ == '__main__':
    run_cli(CLAIM, check)
