import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe7-every-summary', 'artifact': 'episode', 'type': 'objection', 'story': 'Astra feedback', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'only the summary statement is captured')
    if not ctx.art_has(r'(?is)Every.{0,120}(?:summary only|only.{0,30}summary|summary.{0,70}(?:not the full|full.{0,20}(?:elsewhere|external|linked)))'): return ctx.fail('framing', q, 'Only Every’s live-testing summary was captured, not the full Vibe Check.')
    return ctx.ok('framing', q)


if __name__ == '__main__':
    run_cli(CLAIM, check)
