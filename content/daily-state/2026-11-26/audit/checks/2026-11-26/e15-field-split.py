import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e15-field-split', 'artifact': 'episode', 'type': 'opinion', 'story': 'Dual-use mathematics', 'quote': 'AI has just turned frontier mathematics into a dual-use technology, splitting the field right down the middle'}


def check(ctx):
    return ctx.need(None, None, 'Historical and field-wide judgment.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
