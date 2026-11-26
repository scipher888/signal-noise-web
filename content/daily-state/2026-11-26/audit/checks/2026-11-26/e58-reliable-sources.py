import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e58-reliable-sources', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Aaronson crypto warning', 'quote': 'from multiple reliable sources'}


def check(ctx):
    return ctx.require('andrewcurran_', r'Scott Aaronson states he is virtually certain, from multiple reliable sources', note='Reported characterization, not verification of sources.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
