import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe6-news-analysis', 'artifact': 'episode', 'type': 'objection', 'story': 'Claude sabotage allegations', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'Third-party news analysis')
    return ctx.ok('framing', q) if ctx.art_has(r'AI Frontier Post[^.]{0,80}(?:report|analysis|notes)|(?:analysis|reporting) (?:by|from) AI Frontier Post|third-party (?:news |reporting )?analysis') else ctx.fail('framing', q, 'Identify the secondary reporting on Schirano’s evidence.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
