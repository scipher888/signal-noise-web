import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e29-one-off-tricks', 'artifact': 'episode', 'type': 'opinion', 'story': 'Tensor geometry', 'quote': 'undercutting the comforting idea that AI only stitches together one-off tricks'}


def check(ctx):
    return ctx.need(None, None, 'Interpretation of the significance of the method.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
