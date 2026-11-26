import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't15-oversight-duration', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Messages API migration', 'quote': 'earning production trust still took five months of human oversight'}


def check(ctx):
    return ctx.need('anthropic', ctx.find('anthropic', r'from April until public traffic moved to Rust in September 2026'), 'Dates bound the migration work. They do not isolate the time spent earning trust under human oversight.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
