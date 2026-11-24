import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't04-qualifier-nearly-12x', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Google DeepMind quantum circuits', 'quote': 'nearly 12 times'}


def check(ctx):
    return ctx.require('deepmind', r'11\.8×')


if __name__ == '__main__':
    run_cli(CLAIM, check)
