import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's18-verifiability-split-opinion', 'artifact': 'short', 'type': 'opinion', 'story': 'AI Verifiability Split', 'quote': 'where a compiler checks the work, human understanding is optional. Everywhere else, human judgment is still the ceiling.'}


def check(ctx):
    return ctx.need(None, None, 'Editorial opinion/synthesis on verifiable vs. unverifiable tasks; requires human judgment')


if __name__ == '__main__':
    run_cli(CLAIM, check)
