import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e13-built-for-search', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Discovery vs. reliability', 'quote': 'built for problems where you only need one hit out of many tries and an outside check discards the misses'}


def check(ctx):
    return ctx.need('openai', ctx.find('openai', r'We can design far more proteins on a computer than we can make and test'), '“Built for” one-hit discovery with an outside check is an interpretation of training and workflow, not a stated design goal.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
