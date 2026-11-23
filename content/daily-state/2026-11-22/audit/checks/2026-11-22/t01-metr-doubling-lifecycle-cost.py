import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't01-metr-doubling-lifecycle-cost', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'METR AI agent time horizon', 'quote': "METR found that doubling a task's lifecycle cost cuts an AI agent's effective time horizon roughly in half"}


def check(ctx):
    return ctx.require('metr', r'doubling of lifecycle cost.*roughly equivalent to halving the time horizon')


if __name__ == '__main__':
    run_cli(CLAIM, check)
