import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's11-250000-plus-pp', 'artifact': 'short', 'type': 'number', 'story': 'Riemann Hypothesis Proof', 'quote': '250,000+ pp'}


def check(ctx):
    return ctx.require('alpoge', r'250,\s*000\+\s*pages')


if __name__ == '__main__':
    run_cli(CLAIM, check)
