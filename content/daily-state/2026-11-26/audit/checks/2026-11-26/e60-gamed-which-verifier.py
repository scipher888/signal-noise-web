import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e60-gamed-which-verifier', 'artifact': 'episode', 'type': 'attribution', 'story': 'Shadow oracle', 'quote': 'an agent still gamed it'}


def check(ctx):
    return ctx.support_or_contradict('anthropic', r'(?:shortcut|fix) passed the (?:outer|production) verifier', r'the fix passed the local verifier', 'The shortcut passed locally; no demonstrated bypass of the production oracle.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
