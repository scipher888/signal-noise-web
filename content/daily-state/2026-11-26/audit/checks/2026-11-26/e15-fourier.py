import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e15-fourier', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Math proofs', 'quote': 'alongside tight Fourier transform bounds'}


def check(ctx):
    return ctx.require('framing', r'(?:tight bounds.{0,30}Fourier transform|tight Fourier transform bounds)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
