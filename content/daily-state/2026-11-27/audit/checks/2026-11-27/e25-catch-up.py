import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e25-catch-up', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Sources of acceleration', 'quote': 'or reflects OpenAI catching up after prioritizing reasoning models over pretraining for several generations'}


def check(ctx):
    return ctx.require('ibab', r'likely confounded by OpenAI lagging behind on pretraining tech for a few generations and catching up now', r'appears they neglected pretraining in favor of reasoning progress')


if __name__ == '__main__':
    run_cli(CLAIM, check)
