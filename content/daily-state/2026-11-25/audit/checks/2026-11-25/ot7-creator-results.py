import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot7-creator-results', 'artifact': 'takeaways', 'type': 'objection', 'story': "Humanity's First Exam", 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'Benchmark creator.s own leaderboard and summary of its paper')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:creator.s own|DeepMind.s own|Google.s own).{0,48}(?:leaderboard|results|paper)|(?:DeepMind|Kaggle).{0,35}(?:reports|summarizes|published).{0,32}(?:its own|its paper|its leaderboard)') else ctx.fail('framing', q, 'Clarify provenance of scores, not just benchmark ownership.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
