import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't17-intent-hacking', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Benchmarks and builder reports', 'quote': 'Zvi Mowshowitz and user reports flag struggles with human intent and reward hacking'}


def check(ctx):
    return ctx.require('thezvi', r'biggest complaint.*failure to understand user intent', r'worry about various forms of reward hacking', r'does not understand human intent whatsoever', r'Reward hacks.*personal benchmarks')


if __name__ == '__main__':
    run_cli(CLAIM, check)
