import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e07-openai-preprint', 'artifact': 'episode', 'type': 'attribution', 'story': 'Protein design', 'quote': 'a protein-design preprint from OpenAI'}


def check(ctx):
    return ctx.require('openai2', r'@OpenAI: We.re sharing a new preprint showing wet lab validation of intrinsic protein design capabilities')


if __name__ == '__main__':
    run_cli(CLAIM, check)
