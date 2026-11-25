import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e55-sketchbook-year', 'artifact': 'episode', 'type': 'number', 'story': 'Chabot sketchbook', 'quote': 'an anonymous 1808 sketchbook'}


def check(ctx):
    return ctx.require('gpt62', r'an anonymous 1808 sketchbook held at Yale.s Beinecke Library')


if __name__ == '__main__':
    run_cli(CLAIM, check)
