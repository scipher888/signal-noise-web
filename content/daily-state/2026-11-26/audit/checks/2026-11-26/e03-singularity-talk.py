import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e03-singularity-talk', 'artifact': 'episode', 'type': 'attribution', 'story': 'Math proofs', 'quote': 'a math avalanche that has top researchers whispering about a singularity'}


def check(ctx):
    return ctx.require('framing', r'(?:leading|top) researchers.{0,100}singularity', note='A roundup of papers does not document researchers saying this.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
