import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e75-public-mood', 'artifact': 'episode', 'type': 'opinion', 'story': 'Disclosure divide', 'quote': 'leaving everyone else swinging between shrugging off abstract math and panicking over half-heard rumors'}


def check(ctx):
    return ctx.need(None, None, 'Editorial description of public sentiment.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
