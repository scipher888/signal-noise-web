import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e35-shapes-sequences', 'artifact': 'episode', 'type': 'attribution', 'story': 'Protein design', 'quote': 'OpenAI reports that its GPT-6 models can design protein shapes and sequences'}


def check(ctx):
    return ctx.require('openai', r'Our GPT.6 family of models can design new protein shapes and the sequence of their chemical building blocks')


if __name__ == '__main__':
    run_cli(CLAIM, check)
