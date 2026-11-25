import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e62-ordered-scans', 'artifact': 'episode', 'type': 'attribution', 'story': 'Chabot sketchbook', 'quote': 'Humphries ordered the scans'}


def check(ctx):
    return ctx.require('gpt62', r'But order the journal I did', r'all three documents arrived in my inbox')


if __name__ == '__main__':
    run_cli(CLAIM, check)
