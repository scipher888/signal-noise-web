import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e63-matched-prompts', 'artifact': 'episode', 'type': 'comparison', 'story': 'Shadow oracle', 'quote': 'The outputs matched'}


def check(ctx):
    return ctx.require('anthropic', r'The prompts then matched, and the fix passed the local verifier', note='Outputs of local prompt construction, not production model replies.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
