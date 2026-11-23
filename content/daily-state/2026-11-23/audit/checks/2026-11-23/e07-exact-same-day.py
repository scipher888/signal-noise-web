import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e07-exact-same-day', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Overview', 'quote': 'on the exact same day'}


def check(ctx):
    s = ctx.find('openai', r'November 22, 2026')
    return ctx.need('openai', s, 'OpenAI post is dated November 22, 2026, but LingSante sources do not print a calendar date in text')


if __name__ == '__main__':
    run_cli(CLAIM, check)
