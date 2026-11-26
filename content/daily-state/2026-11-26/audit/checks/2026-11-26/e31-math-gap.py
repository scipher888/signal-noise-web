import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e31-math-gap', 'artifact': 'episode', 'type': 'opinion', 'story': 'Proof verification', 'quote': 'mathematics has a generator-verifier gap that favors AI'}


def check(ctx):
    return ctx.need('anthropic', ctx.find('anthropic', r'Claude projects have relied on this gap: formalizing proofs in mathematics'), 'Generalization about AI advantage.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
