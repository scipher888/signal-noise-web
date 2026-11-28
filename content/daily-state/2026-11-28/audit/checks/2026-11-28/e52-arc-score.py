import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e52-arc-score', 'artifact': 'episode', 'type': 'number', 'story': 'Astra benchmarks', 'quote': '100 percent on ARC-AGI-3'}


def check(ctx):
    return ctx.require('thezvi', r'ARC-AGI-3: 100\.0% \(SOTA\).*provider adapter')


if __name__ == '__main__':
    run_cli(CLAIM, check)
