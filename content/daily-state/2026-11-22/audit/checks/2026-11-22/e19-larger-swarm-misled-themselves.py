import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e19-larger-swarm-misled-themselves', 'artifact': 'episode', 'type': 'comparison', 'story': 'METR capability update', 'quote': 'the larger the swarm got, the more confidently the agents misled themselves'}


def check(ctx):
    return ctx.require('metr', r'as swarm size increases.*larger swarms were more prone to misleading themselves')


if __name__ == '__main__':
    run_cli(CLAIM, check)
