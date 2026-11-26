import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e23-aaronson-confidence', 'artifact': 'episode', 'type': 'attribution', 'story': 'Factoring rumor', 'quote': 'Aaronson confirmed he is virtually certain, from multiple reliable sources, that frontier labs hold unreleased cryptography bombshells'}


def check(ctx):
    q = ctx.find('andrewcurran_', r'Scott Aaronson states he is virtually certain, from multiple reliable sources, that frontier labs hold unreleased cryptography .bombshells')
    return ctx.need('andrewcurran_', q, 'The wording is in a Grok reply; verify Aaronson’s own statement and level of confidence.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
