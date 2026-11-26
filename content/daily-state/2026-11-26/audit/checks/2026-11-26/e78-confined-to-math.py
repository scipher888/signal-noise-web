import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e78-confined-to-math', 'artifact': 'episode', 'type': 'attribution', 'story': 'Aaronson Thanksgiving advice', 'quote': 'hoping we get lucky and it stays confined to hard math'}


def check(ctx):
    return ctx.require('framing', r'(?=.*Aaronson)(?=.*(?:hope|hoping|lucky))(?=.*(?:confined|limited|restricted) to hard math)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
