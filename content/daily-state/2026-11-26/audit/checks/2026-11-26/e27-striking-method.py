import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e27-striking-method', 'artifact': 'episode', 'type': 'comparison', 'story': 'Tensor geometry', 'quote': 'Just as striking as the answers is how OpenAI reached them'}


def check(ctx):
    return ctx.need(None, None, 'Relative strikingness is subjective.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
