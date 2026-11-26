import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e39-wrong-statement', 'artifact': 'episode', 'type': 'comparison', 'story': 'Proof verification', 'quote': 'rather than the AI proving something technically valid that misses the point'}


def check(ctx):
    return ctx.need('anthropic', ctx.find('anthropic', r'A theorem in mathematics is a precise statement'), 'Step checking alone does not document a mismatch with an intended conjecture.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
