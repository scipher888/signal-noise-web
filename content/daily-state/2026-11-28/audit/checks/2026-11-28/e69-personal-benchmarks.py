import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e69-personal-benchmarks', 'artifact': 'episode', 'type': 'attribution', 'story': 'Astra feedback', 'quote': 'reward-hacks personal benchmarks it could solve honestly'}


def check(ctx):
    return ctx.require('thezvi', r'Reward hacks.*personal benchmarks.*sol and astra 6\.2 both do.*they can solve it without cheating')


if __name__ == '__main__':
    run_cli(CLAIM, check)
