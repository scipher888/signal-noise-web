import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e65-returned-diary', 'artifact': 'episode', 'type': 'attribution', 'story': 'Chabot sketchbook', 'quote': 'Humphries gave that proof back to Astra'}


def check(ctx):
    return ctx.require('gpt62', r'When given a copy of the diary, which proved the case.*Astra started to hedge')


if __name__ == '__main__':
    run_cli(CLAIM, check)
