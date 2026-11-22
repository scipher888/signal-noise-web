import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e17-swarms-beat-independent-nanogpt', 'artifact': 'episode', 'type': 'comparison', 'story': 'METR capability update', 'quote': 'On NanoGPT optimization, where agents get an exact score back quickly, swarms beat independent agents'}


def check(ctx):
    return ctx.require('metr', r'swarm uplift.*nanoGPT', r'exact grade for each submission', r'Swarms.*outperform best-of-k.*nanoGPT')


if __name__ == '__main__':
    run_cli(CLAIM, check)
