import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e54-lean-complete', 'artifact': 'episode', 'type': 'attribution', 'story': 'Google formalizations', 'quote': 'companion Lean 4 formalizations it says are complete'}


def check(ctx):
    return ctx.support_or_contradict('google', r'Lean 4 formalizations .*?(?:are|have been) completed', r'formalization of the\s+entire proof has also been completed', 'Completion is claimed for the singular log-rank formalization, not the whole set.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
