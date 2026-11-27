import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't16-commercial', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Claude refusal behavior', 'quote': 'commercial refusal classifier'}


def check(ctx):
    return ctx.require('framing', r'(?:docs|documentation).*(?:commercial refusal classifier|refusal classifier.*commercial restriction)', note='Company provenance does not establish commercial purpose.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
