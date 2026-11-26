import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e25-beating-fft', 'artifact': 'episode', 'type': 'comparison', 'story': 'Fourier transform', 'quote': 'beating the classic 1960s Fast Fourier Transform'}


def check(ctx):
    return ctx.require('framing', r'(?=.*(?:beat\w*|improv\w* on|fewer .*than))(?=.*1960s)(?=.*(?:fast Fourier transform|FFT))')


if __name__ == '__main__':
    run_cli(CLAIM, check)
