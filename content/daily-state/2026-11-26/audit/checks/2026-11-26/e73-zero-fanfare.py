import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e73-zero-fanfare', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Disclosure divide', 'quote': 'with zero fanfare'}


def check(ctx):
    return ctx.require('framing', r'(?=.*(?:labs|papers))(?=.*(?:no publicity|without (?:any )?publicity|without fanfare))', note='Repository publication is not evidence of zero publicity.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
