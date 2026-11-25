import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot9-two-cohorts', 'artifact': 'takeaways', 'type': 'objection', 'story': "Humanity's First Exam", 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'leaderboard lists 16 models while the X post cites 18 from the paper')
    board = ctx.art_has(r'(?:leaderboard|Kaggle run).{0,40}(?:16|sixteen) models|(?:16|sixteen)[- ]model leaderboard')
    paper = ctx.art_has(r'(?:paper|X post).{0,45}(?:18|eighteen)(?: models)?|(?:18|eighteen)[- ]model (?:paper|study)')
    return ctx.ok('framing', q) if board and paper else ctx.fail('framing', q, 'Distinguish the leaderboard’s 16 from the paper’s 18.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
