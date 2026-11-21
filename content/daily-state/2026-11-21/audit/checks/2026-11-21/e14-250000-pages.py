import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e14-250000-pages', 'artifact': 'episode', 'type': 'number', 'story': 'Riemann Hypothesis proof', 'quote': 'more than two hundred and fifty thousand pages'}


def check(ctx):
    return ctx.require('alpoge', r'250,\s*000\+\s*pages')


if __name__ == '__main__':
    run_cli(CLAIM, check)
