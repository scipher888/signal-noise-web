import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e08-derek-thompson-quote', 'artifact': 'episode', 'type': 'attribution', 'story': 'Riemann Hypothesis proof', 'quote': "The journalist Derek Thompson called it the cleanest possible example that AI capabilities don't automatically equal real-world consequences"}


def check(ctx):
    return ctx.require('dkthomp', r'cleaner example.*AI capabilities.*real-world AI consequences')


if __name__ == '__main__':
    run_cli(CLAIM, check)
