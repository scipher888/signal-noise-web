import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e03-mystery-age', 'artifact': 'episode', 'type': 'number', 'story': 'Chabot sketchbook', 'quote': 'a 218-year-old historical mystery'}


def check(ctx):
    q = ctx.find('gpt62', r'document has remained anonymous for more than 200 years')
    if not ctx.find('gpt62', r'anonymous 1808 sketchbook') or not ctx.find('gpt62', r'Nov 24, 2026'):
        return ctx.need('gpt62', q, 'Need the sketchbook date and the post date to assess the 218-year figure.')
    return ctx.need('gpt62', q, 'Source dates the sketchbook to 1808 and says it remained anonymous more than 200 years; it does not state 218 years.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
