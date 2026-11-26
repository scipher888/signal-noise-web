import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e30-github-theorems', 'artifact': 'episode', 'type': 'attribution', 'story': 'Math proofs', 'quote': 'labs drop major theorems straight onto GitHub'}


def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'Company-posted preprints in a public repository'), 'One lab’s repository does not establish the broader practice or theorem status.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
