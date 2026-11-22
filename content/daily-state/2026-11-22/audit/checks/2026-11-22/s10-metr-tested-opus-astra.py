import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's10-metr-tested-opus-astra', 'artifact': 'short', 'type': 'attribution', 'story': 'AI Verification & Riemann Proof', 'quote': 'METR tested Opus 5.5 and GPT-6 Astra'}


def check(ctx):
    return ctx.require('metr', r'up to Opus 5\.5 and GPT-6 Astra')


if __name__ == '__main__':
    run_cli(CLAIM, check)
