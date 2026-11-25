import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e63-handwriting', 'artifact': 'episode', 'type': 'attribution', 'story': 'Chabot sketchbook', 'quote': 'matched the handwriting'}


def check(ctx):
    return ctx.require('gpt62', r'handwriting, which featured the same distinctive letter forms as the sketchbook')


if __name__ == '__main__':
    run_cli(CLAIM, check)
