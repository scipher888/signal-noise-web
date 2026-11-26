import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e09-hyperspace', 'artifact': 'episode', 'type': 'comparison', 'story': 'Math proofs', 'quote': 'mathematics suddenly looks like hyperspace'}


def check(ctx):
    return ctx.need(None, None, 'Figurative comparison.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
