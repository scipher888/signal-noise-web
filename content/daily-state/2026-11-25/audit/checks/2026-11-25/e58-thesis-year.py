import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e58-thesis-year', 'artifact': 'episode', 'type': 'number', 'story': 'Chabot sketchbook', 'quote': 'a 2014 thesis footnote'}


def check(ctx):
    return ctx.require('gpt62', r'a single footnote in a 2014 PhD thesis')


if __name__ == '__main__':
    run_cli(CLAIM, check)
