import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot3-retrieval-date', 'artifact': 'takeaways', 'type': 'objection', 'story': 'Claude refusal behavior', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'published_date is the retrieval date')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:retrieval|access|snapshot) date[^.]{0,80}not[^.]{0,25}release|(?:retrieved|accessed)[^.]{0,100}not[^.]{0,25}release') else ctx.fail('framing', q, 'Docs date is retrieval, not release.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
