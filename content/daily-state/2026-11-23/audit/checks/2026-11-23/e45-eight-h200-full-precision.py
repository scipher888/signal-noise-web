import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e45-eight-h200-full-precision', 'artifact': 'episode', 'type': 'number', 'story': 'Ant Group LingSante', 'quote': 'eight H200 GPUs—to run at full precision'}


def check(ctx):
    s = ctx.find('antlingagi', r'Official FP8 weights.*8.?\s*H200')
    if s and ctx.absent('lingsante', r'full precision'):
        return ctx.fail('antlingagi', s, 'Sources specify 8x H200 for FP8 weights, not full precision')
    return ctx.require('lingsante', r'8\s*[×x]\s*H200', r'full precision')


if __name__ == '__main__':
    run_cli(CLAIM, check)
