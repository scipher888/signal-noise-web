import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e32-lean-rules', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Proof verification', 'quote': 'a proof assistant like Lean offers a fixed, explicit rulebook'}


def check(ctx):
    return ctx.require('anthropic', r'proof assistant \(like Lean\) can check each step of a proof against a fixed set of rules')


if __name__ == '__main__':
    run_cli(CLAIM, check)
