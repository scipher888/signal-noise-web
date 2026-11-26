import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't16-five-months', 'artifact': 'takeaways', 'type': 'number', 'story': 'Messages API migration', 'quote': 'five months of human oversight'}


def check(ctx):
    return ctx.need('anthropic', ctx.find('anthropic', r'from April until public traffic moved to Rust in September 2026'), 'Five named-month intervals; chart measures merged changes, not a duration of oversight.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
