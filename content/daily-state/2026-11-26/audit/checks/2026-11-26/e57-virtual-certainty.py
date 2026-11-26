import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e57-virtual-certainty', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Aaronson crypto warning', 'quote': 'virtually certain'}


def check(ctx):
    return ctx.require('andrewcurran_', r'Scott Aaronson states he is virtually certain.*unreleased cryptography', note='Reported confidence about unspecified results.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
