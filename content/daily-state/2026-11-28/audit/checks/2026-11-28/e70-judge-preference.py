import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e70-judge-preference', 'artifact': 'episode', 'type': 'attribution', 'story': 'Astra feedback', 'quote': "even persuades other AI models acting as judges to prefer Astra's weaker drafts"}


def check(ctx):
    q = ctx.find('thezvi', r'all voted for Astra.s lyrics, which were IMO substantially worse')
    if q: return ctx.fail('thezvi', q, 'A preference vote and one user’s assessment of quality do not establish persuasion or objectively weaker drafts.')
    return ctx.require('thezvi', r'persuaded.*judges.*weaker drafts')


if __name__ == '__main__':
    run_cli(CLAIM, check)
