import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e64-verifier-pass', 'artifact': 'episode', 'type': 'attribution', 'story': 'Shadow oracle', 'quote': 'The verifier said pass'}


def check(ctx):
    return ctx.require('anthropic', r'The prompts then matched, and the fix passed the local verifier', note='Local verifier only.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
