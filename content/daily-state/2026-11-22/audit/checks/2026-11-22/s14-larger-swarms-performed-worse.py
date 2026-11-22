import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's14-larger-swarms-performed-worse', 'artifact': 'short', 'type': 'comparison', 'story': 'AI Verification & Riemann Proof', 'quote': 'Without a fast ground-truth check, larger agent swarms actually performed worse'}


def check(ctx):
    return ctx.require('metr', r'without a ground truth', r'increasing swarm size resulted in decreasing scores')


if __name__ == '__main__':
    run_cli(CLAIM, check)
