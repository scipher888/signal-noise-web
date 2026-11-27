import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e39-unread-disclosure', 'artifact': 'episode', 'type': 'attribution', 'story': 'Claude sabotage allegations', 'quote': "Schirano later admitted he had not read Anthropic's November 9th disclosure for Claude Fable 5.2 and Mythos 5.2"}


def check(ctx):
    return ctx.require('claude', r'November 9 launch of Fable 5\.2 and Mythos 5\.2', r'Anthropic.s November disclosure.*Never seen this before.*he had not read it before posting')


if __name__ == '__main__':
    run_cli(CLAIM, check)
