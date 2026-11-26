import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't20-multiple-sources', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'RSA rumors', 'quote': 'multiple reliable sources'}


def check(ctx):
    return ctx.require('andrewcurran_', r'Scott Aaronson states he is virtually certain, from multiple reliable sources', note='Attribution of confidence, not authentication.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
