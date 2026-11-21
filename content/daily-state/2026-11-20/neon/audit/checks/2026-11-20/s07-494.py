import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's07-494', 'artifact': 'short', 'type': 'number', 'story': 'Society', 'quote': '49.4%'}


def check(ctx):
    return ctx.require('society', r'77 of 156 cases \(49\.4%\)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
