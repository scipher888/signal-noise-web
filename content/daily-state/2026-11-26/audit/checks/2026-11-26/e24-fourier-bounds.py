import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e24-fourier-bounds', 'artifact': 'episode', 'type': 'comparison', 'story': 'Fourier transform', 'quote': 'matching upper and lower bounds'}


def check(ctx):
    return ctx.require('framing', r'(?=.*Fourier)(?=.*linear gates)(?=.*matching (?:upper and lower|lower and upper) bounds)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
