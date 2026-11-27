import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e37-viral-threads', 'artifact': 'episode', 'type': 'attribution', 'story': 'Claude sabotage allegations', 'quote': 'set off other viral threads blaming Claude, and sometimes GPT, for ruined training runs'}


def check(ctx):
    q = ctx.find('realastropulse', r'After seeing the .Claude sabotages your ML research. posts')
    g = ctx.find('ptrcast', r'hear rumors about claude/GPT sabotaging ML work')
    return ctx.need('realastropulse', q, 'Related anecdotes, but verify their reach, ruined runs, and causal link to this specific post. ' + (g or ''))


if __name__ == '__main__':
    run_cli(CLAIM, check)
