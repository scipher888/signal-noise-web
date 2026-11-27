import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e53-error-alerts', 'artifact': 'episode', 'type': 'qualifier', 'story': 'API refusal and fallback behavior', 'quote': 'standard HTTP 200 responses that normal error alerts miss'}


def check(ctx):
    return ctx.require('framing', r'HTTP 200.*(?:miss|not trigger|bypass).*error alerts', note='Need evidence on status and alert behavior.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
