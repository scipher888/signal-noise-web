import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e07-same-day', 'artifact': 'episode', 'type': 'comparison', 'story': 'Two headlines', 'quote': "Published the very same day as the math panic, Anthropic's post"}


def check(ctx):
    a = ctx.find('anthropic', r'Published\s*Nov 25, 2026')
    b = ctx.find('framing', r'(?:math panic|Aaronson.s (?:post|blog)).{0,60}Nov(?:ember)? 25, 2026')
    return ctx.ok('framing', b, str(a)) if a and b else ctx.need('anthropic', a, 'Need a dated math event, not just the date of the scan.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
