import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e38-no-materials', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Claude sabotage allegations', 'quote': 'None of those viral posts shared prompts, code, or logs'}


def check(ctx):
    q = ctx.find('realastropulse', r'personal anecdote with screenshots, no shared code or logs')
    return ctx.need('realastropulse', q, 'Verify prompts, code and logs across all cited posts, including linked threads; one scan note does not settle the universal negative.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
