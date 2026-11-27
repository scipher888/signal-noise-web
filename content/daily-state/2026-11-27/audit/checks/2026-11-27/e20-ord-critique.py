import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e20-ord-critique', 'artifact': 'episode', 'type': 'attribution', 'story': 'METR chart debate', 'quote': 'Oxford philosopher Toby Ord criticized it on that basis'}


def check(ctx):
    return ctx.require('tobyordoxford', r'Oxford philosopher who had publicly criticized the post', r'When I was critical of it, I was indeed treating it as a METR research finding')


if __name__ == '__main__':
    run_cli(CLAIM, check)
