import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e26-fft-decade', 'artifact': 'episode', 'type': 'number', 'story': 'Fourier transform', 'quote': 'classic 1960s Fast Fourier Transform'}


def check(ctx):
    return ctx.require('framing', r'(?=.*(?:1960s|196[0-9]\b))(?=.*(?:fast Fourier transform|Cooley.Tukey FFT))')


if __name__ == '__main__':
    run_cli(CLAIM, check)
