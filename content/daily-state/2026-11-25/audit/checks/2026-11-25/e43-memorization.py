import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e43-memorization', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Protein design', 'quote': 'suggesting this goes beyond memorization'}


def check(ctx):
    return ctx.require('openai', r'unpublished structures and substantial differences in sequence give us strong evidence that GPT.6\.2.s capabilities extend beyond memorization')


if __name__ == '__main__':
    run_cli(CLAIM, check)
