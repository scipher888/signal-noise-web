import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e38-looping-doubled-no-cot-horizon', 'artifact': 'episode', 'type': 'comparison', 'story': 'Inkling 2 Mini', 'quote': "looping doubled the model's no-chain-of-thought horizon"}


def check(ctx):
    return ctx.require('thinking', r'no-CoT time horizon.*from 16 seconds at one pass to 37 seconds')


if __name__ == '__main__':
    run_cli(CLAIM, check)
