import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e36-reasoning-code', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Protein design', 'quote': 'using only reasoning and code'}


def check(ctx):
    return ctx.require('openai', r'design new protein shapes.*using only reasoning and code')


if __name__ == '__main__':
    run_cli(CLAIM, check)
