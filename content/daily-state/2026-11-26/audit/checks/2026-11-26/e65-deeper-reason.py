import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e65-deeper-reason', 'artifact': 'episode', 'type': 'opinion', 'story': 'Dual-use mathematics', 'quote': 'the math deluge and the cryptography rumors collided this week for a deeper reason'}


def check(ctx):
    return ctx.need(None, None, 'Interpretive causal thesis.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
