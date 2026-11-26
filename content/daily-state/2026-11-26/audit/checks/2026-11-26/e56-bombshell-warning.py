import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e56-bombshell-warning', 'artifact': 'episode', 'type': 'attribution', 'story': 'Aaronson crypto warning', 'quote': 'He wrote that he is virtually certain, from multiple reliable sources, that frontier labs are sitting on one or more unreleased cryptographic bombshells'}


def check(ctx):
    return ctx.require('andrewcurran_', r'Scott Aaronson states he is virtually certain, from multiple reliable sources, that frontier labs hold unreleased cryptography ["“]bombshells', note='Secondary attribution in a reply; plural entails at least one. Not lab confirmation.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
