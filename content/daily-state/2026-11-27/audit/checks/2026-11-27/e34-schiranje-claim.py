import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e34-schiranje-claim', 'artifact': 'episode', 'type': 'attribution', 'story': 'Claude sabotage allegations', 'quote': 'former engineer Pietro Schirano posted on X that Claude tries to sabotage research at every stage'}


def check(ctx):
    return ctx.require('claude', r'former Anthropic engineer, Pietro Schirano, posted.*Claude tries to .sabotage. research work at every stage', r'Schirano.s X post')


if __name__ == '__main__':
    run_cli(CLAIM, check)
