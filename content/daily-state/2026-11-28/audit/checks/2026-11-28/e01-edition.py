import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e01-edition', 'artifact': 'episode', 'type': 'number', 'story': 'Edition', 'quote': 'Daily State of AI for Saturday, November 28th, 2026'}


def check(ctx):
    return ctx.require('framing', r'(?:Saturday,?\s+November 28(?:th)?,? 2026|2026-11-28)', note='Edition date, not the date of the malware scan.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
