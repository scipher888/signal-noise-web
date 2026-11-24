import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e33-zero-days-six-year-low', 'artifact': 'episode', 'type': 'number', 'story': 'CSET Cyber Report', 'quote': 'zero-days exploited in the wild are on pace for a six-year low'}


def check(ctx):
    return ctx.require('openai', r'zero-day vulnerabilities.*2026 on pace to be the lowest in six years')


if __name__ == '__main__':
    run_cli(CLAIM, check)
