import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't21-unreleased', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'RSA rumors', 'quote': 'unreleased'}


def check(ctx):
    return ctx.require('andrewcurran_', r'Scott Aaronson states .*frontier labs hold unreleased cryptography', note='Within the reported warning only.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
