import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e16-silent-commit', 'artifact': 'episode', 'type': 'attribution', 'story': 'Google papers', 'quote': 'Then Google Research silently committed six papers'}


def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'Google Research posts six Cogentic papers'), 'Posting is documented; silence and sequence are not.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
