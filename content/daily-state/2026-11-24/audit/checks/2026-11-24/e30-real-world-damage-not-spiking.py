import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e30-real-world-damage-not-spiking', 'artifact': 'episode', 'type': 'comparison', 'story': 'CSET Cyber Report', 'quote': 'real-world cyber damage is not spiking'}


def check(ctx):
    return ctx.require('openai', r'data on real-world impacts of cyber attacks tells a less dire story')


if __name__ == '__main__':
    run_cli(CLAIM, check)
