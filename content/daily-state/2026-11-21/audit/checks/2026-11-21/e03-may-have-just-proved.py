import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e03-may-have-just-proved', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Riemann Hypothesis proof', 'quote': 'may have just proved'}


def check(ctx):
    return ctx.require('alpoge', r'I believe I have, working with Claude, discovered a proof')


if __name__ == '__main__':
    run_cli(CLAIM, check)
