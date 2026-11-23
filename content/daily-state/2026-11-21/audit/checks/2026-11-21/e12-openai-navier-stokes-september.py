import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e12-openai-navier-stokes-september', 'artifact': 'episode', 'type': 'attribution', 'story': 'Riemann Hypothesis proof', 'quote': "OpenAI's claimed Navier-Stokes proof back in September"}


def check(ctx):
    return ctx.require('artificialanlys', r'OpenAI.*claimed a solution to the Navier-Stokes problem in September')


if __name__ == '__main__':
    run_cli(CLAIM, check)
