import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e51-esmfold-comparison', 'artifact': 'episode', 'type': 'comparison', 'story': 'Protein design', 'quote': 'compared with 0.93 for the specialist model ESMFold2'}


def check(ctx):
    return ctx.require('openai', r'0\.38 for our latest internal model', r'The specialized model ESMFold2 averaged 0\.93')


if __name__ == '__main__':
    run_cli(CLAIM, check)
