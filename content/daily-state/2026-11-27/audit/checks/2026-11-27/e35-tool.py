import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e35-tool', 'artifact': 'episode', 'type': 'attribution', 'story': 'Claude sabotage allegations', 'quote': 'saying he built a tool called Do Not Sabotage to reroute tasks to rivals'}


def check(ctx):
    return ctx.require('claude', r'He said.*he built a skill, .DoNotSabotage,. that routes his Claude work to rival models instead')


if __name__ == '__main__':
    run_cli(CLAIM, check)
