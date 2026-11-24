import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e25-operator-approval', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Linux Cybersecurity', 'quote': 'an operator still has to approve each shield and make sure it does not break legitimate traffic'}


def check(ctx):
    return ctx.require('openai', r'operator.*approve.*shield', note='Primary Shirudo source not in snapshot')


if __name__ == '__main__':
    run_cli(CLAIM, check)
