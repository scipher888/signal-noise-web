import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e80-bottleneck', 'artifact': 'episode', 'type': 'opinion', 'story': 'Model supervision', 'quote': 'Across local desktops and frontier APIs alike, raw capability is no longer the bottleneck'}


def check(ctx):
    return ctx.need('thezvi', ctx.find('thezvi', r'for many practical purposes other differences now matter a lot more'), 'Cross-platform bottleneck judgment, not a measured comparison.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
