import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't19-virtually-certain', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'RSA rumors', 'quote': 'virtually certain'}


def check(ctx):
    return ctx.require('andrewcurran_', r'Scott Aaronson states he is virtually certain.*unreleased cryptography', note='Confidence concerns unspecified bombshells.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
