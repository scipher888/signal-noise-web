import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e17-naam-viral-post-title', 'artifact': 'episode', 'type': 'attribution', 'story': 'AI task-horizon analysis', 'quote': "Ramez Naam's viral post today, titled The Most Important Charts in AI are Wrong"}


def check(ctx):
    return ctx.require('naam', r'The Most Important Charts in AI are Wrong', r'Ramez Naam', r'Nov 21, 2026')


if __name__ == '__main__':
    run_cli(CLAIM, check)
