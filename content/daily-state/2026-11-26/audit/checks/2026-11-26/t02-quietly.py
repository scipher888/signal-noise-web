import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't02-quietly', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Cogentic papers', 'quote': 'quietly'}


def check(ctx):
    return ctx.require('framing', r'(?=.*Google Research)(?=.*(?:quietly|without (?:an )?announcement|unannounced))')


if __name__ == '__main__':
    run_cli(CLAIM, check)
