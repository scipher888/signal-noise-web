import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't21-esmfold-score', 'artifact': 'takeaways', 'type': 'number', 'story': 'GPT-6 protein binders', 'quote': '0.93 for ESMFold2'}


def check(ctx):
    return ctx.require('openai', r'The specialized model ESMFold2 averaged 0\.93')


if __name__ == '__main__':
    run_cli(CLAIM, check)
