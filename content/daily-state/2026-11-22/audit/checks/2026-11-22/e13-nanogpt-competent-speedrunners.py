import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e13-nanogpt-competent-speedrunners', 'artifact': 'episode', 'type': 'comparison', 'story': 'METR capability update', 'quote': 'beat competent human speedrunners on NanoGPT at a fraction of the cost'}


def check(ctx):
    return ctx.require('metr', r'NanoGPT', r'outperform.*competent speedrunners.*costing less')


if __name__ == '__main__':
    run_cli(CLAIM, check)
