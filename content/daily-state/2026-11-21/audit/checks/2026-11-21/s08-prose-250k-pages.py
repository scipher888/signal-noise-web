import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's08-prose-250k-pages', 'artifact': 'short', 'type': 'number', 'story': 'Riemann Hypothesis Proof', 'quote': 'Prose hit two hundred fifty thousand pages'}


def check(ctx):
    return ctx.require('alpoge', r'250,\s*000\+\s*pages')


if __name__ == '__main__':
    run_cli(CLAIM, check)
