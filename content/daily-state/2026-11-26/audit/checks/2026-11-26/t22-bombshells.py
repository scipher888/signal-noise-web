import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't22-bombshells', 'artifact': 'takeaways', 'type': 'opinion', 'story': 'RSA rumors', 'quote': 'cryptographic bombshells'}


def check(ctx):
    return ctx.need('andrewcurran_', ctx.find('andrewcurran_', r'unreleased cryptography ["“]bombshells'), 'The metaphor is reported; its assessment of significance is subjective.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
