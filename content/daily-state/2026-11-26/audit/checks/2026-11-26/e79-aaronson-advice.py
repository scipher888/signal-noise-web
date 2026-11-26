import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e79-aaronson-advice', 'artifact': 'episode', 'type': 'attribution', 'story': 'Aaronson Thanksgiving advice', 'quote': 'For today, he offered simpler advice: spend Thanksgiving with the people you love'}


def check(ctx):
    return ctx.require('framing', r'(?=.*Aaronson)(?=.*spend Thanksgiving with (?:the people you love|your loved ones))')


if __name__ == '__main__':
    run_cli(CLAIM, check)
