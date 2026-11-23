import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e50-twelve-humans', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Blueprint', 'quote': 'whether a leaderboard edges past twelve humans'}


def check(ctx):
    return ctx.support_or_contradict('blueprint', r'(12|twelve) (humans|people|participants)', r'Human baseline tested on subset of 12 apartments',
        'the 12 is apartments in the human-baseline subset, not twelve humans')


if __name__ == '__main__':
    run_cli(CLAIM, check)
