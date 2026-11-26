import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't18-aaronson-confidence', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'RSA rumors', 'quote': 'he wrote he is virtually certain from multiple reliable sources that labs are holding unreleased cryptographic bombshells'}


def check(ctx):
    return ctx.require('andrewcurran_', r'Scott Aaronson states he is virtually certain, from multiple reliable sources, that frontier labs hold unreleased cryptography ["“]bombshells', note='Secondary account of his statement, not independent confirmation.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
