import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e59-one-or-more', 'artifact': 'episode', 'type': 'number', 'story': 'Aaronson crypto warning', 'quote': 'one or more unreleased cryptographic bombshells'}


def check(ctx):
    return ctx.require('andrewcurran_', r'Scott Aaronson states .*frontier labs hold unreleased cryptography ["“]bombshells', note='Plural supports one or more within the attributed warning only.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
