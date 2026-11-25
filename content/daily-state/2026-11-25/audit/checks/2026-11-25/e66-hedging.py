import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e66-hedging', 'artifact': 'episode', 'type': 'attribution', 'story': 'Chabot sketchbook', 'quote': 'the model strangely hedged and doubted its own find because the diary was unsigned'}


def check(ctx):
    return ctx.require('gpt62', r'Astra started to hedge.*because the diary was not signed, it might not be Chabot.s')


if __name__ == '__main__':
    run_cli(CLAIM, check)
