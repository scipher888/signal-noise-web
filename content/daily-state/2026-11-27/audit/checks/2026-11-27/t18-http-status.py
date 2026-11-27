import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't18-http-status', 'artifact': 'takeaways', 'type': 'number', 'story': 'Claude refusal behavior', 'quote': 'return standard HTTP 200 responses'}


def check(ctx):
    return ctx.require('framing', r'refusal.*HTTP 200\b', note='No HTTP status specified in the supplied docs summary.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
