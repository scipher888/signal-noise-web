import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e52-http-status', 'artifact': 'episode', 'type': 'number', 'story': 'API refusal and fallback behavior', 'quote': 'refusals arrive as standard HTTP 200 responses'}


def check(ctx):
    return ctx.require('framing', r'refusal.*HTTP 200\b', note='Verify the status for refusals in the missing API text.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
