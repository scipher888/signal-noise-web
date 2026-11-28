import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e66-literal-genie', 'artifact': 'episode', 'type': 'attribution', 'story': 'Astra feedback', 'quote': 'Users describe a literal genie problem'}


def check(ctx):
    return ctx.require('thezvi', r'like a Genie that does literally what you asked, but not what you wanted', r'takes you far too literally and does not understand human intent')


if __name__ == '__main__':
    run_cli(CLAIM, check)
