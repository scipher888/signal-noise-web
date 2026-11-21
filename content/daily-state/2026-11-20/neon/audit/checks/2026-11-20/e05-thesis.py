import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e05-thesis', 'artifact': 'episode', 'type': 'opinion', 'story': 'Intro', 'quote': 'judging models by prose, prompts, or leaderboard headlines is breaking down'}


def check(ctx):
    s = ctx.find('society', r'Executable Review Finds What Text Can Miss')
    return ctx.need('society', s, 'opinion (episode thesis); nearest supporting source text quoted')


if __name__ == '__main__':
    run_cli(CLAIM, check)
