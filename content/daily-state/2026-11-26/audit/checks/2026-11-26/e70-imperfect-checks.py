import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e70-imperfect-checks', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Production verification', 'quote': 'agents optimize around imperfect checks'}


def check(ctx):
    return ctx.require('anthropic', r'verifier rewarded matching outputs, and the agent found the cheapest way to produce them', r'not whether the fix is good enough to ship')


if __name__ == '__main__':
    run_cli(CLAIM, check)
