import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e24-telephone', 'artifact': 'episode', 'type': 'attribution', 'story': 'Factoring rumor', 'quote': 'he warned specifics can get mangled in a game of Telephone'}


def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'he explicitly declines to vouch for the specifics'), 'Declining to vouch does not document the Telephone explanation.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
