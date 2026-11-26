import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e23-dessert-fourier', 'artifact': 'episode', 'type': 'attribution', 'story': 'Fourier transform', 'quote': 'By dessert, OpenAI added matching upper and lower bounds on the number of linear gates needed for the Fourier transform'}


def check(ctx):
    return ctx.require('framing', r'(?=.*dessert)(?=.*OpenAI)(?=.*matching upper and lower bounds)(?=.*linear gates)(?=.*Fourier transform)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
