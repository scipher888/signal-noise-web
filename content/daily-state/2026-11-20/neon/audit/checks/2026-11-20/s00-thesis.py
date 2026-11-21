import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's00-thesis', 'artifact': 'short', 'type': 'opinion', 'story': 'Intro', 'quote': 'judging models by prose, prompts, or leaderboards is breaking down'}


def check(ctx):
    s = ctx.find('society', r'Executable Review Finds What Text Can Miss')
    return ctx.need('society', s, 'opinion (short thesis); nearest supporting source text quoted')


if __name__ == '__main__':
    run_cli(CLAIM, check)
