import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's05-honest-caveat', 'artifact': 'short', 'type': 'attribution', 'story': 'Society', 'quote': "text-only peer review couldn't tell an honest caveat from a hidden flaw"}


def check(ctx):
    return ctx.require('society', r'could not tell a disclosed weakness from a hidden one')


if __name__ == '__main__':
    run_cli(CLAIM, check)
