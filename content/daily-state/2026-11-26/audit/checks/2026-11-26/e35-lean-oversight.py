import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e35-lean-oversight', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Proof verification', 'quote': "even Lean isn't completely hands-off"}


def check(ctx):
    return ctx.need('anthropic', ctx.find('anthropic', r'proof assistant \(like Lean\) can check each step'), 'Checking steps does not specify which human oversight is necessary.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
