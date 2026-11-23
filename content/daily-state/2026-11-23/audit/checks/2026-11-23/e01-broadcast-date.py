import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e01-broadcast-date', 'artifact': 'episode', 'type': 'number', 'story': 'Overview', 'quote': 'November 23, 2026'}


def check(ctx):
    s = ctx.find('openai', r'November 22, 2026')
    return ctx.need('openai', s, 'Episode date November 23, 2026 is not in source texts; OpenAI post is dated November 22, 2026')


if __name__ == '__main__':
    run_cli(CLAIM, check)
