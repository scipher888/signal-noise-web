import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe14-benchmark-replication', 'artifact': 'episode', 'type': 'objection', 'story': "Humanity's First Exam", 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'leaderboard lists 16 models')
    return ctx.ok('framing', q) if ctx.art_has(r'(?is)(?:benchmark|leaderboard|HFE|DeepMind).{0,160}(?:no independent replication|not (?:yet )?independently replicated)|(?:no independent replication|not independently replicated).{0,50}(?:benchmark|leaderboard|HFE)') else ctx.fail('framing', q, 'Disclose no independent replication of benchmark results.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
