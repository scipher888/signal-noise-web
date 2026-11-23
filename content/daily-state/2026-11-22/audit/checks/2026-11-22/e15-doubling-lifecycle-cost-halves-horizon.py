import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e15-doubling-lifecycle-cost-halves-horizon', 'artifact': 'episode', 'type': 'comparison', 'story': 'METR capability update', 'quote': "Even when you control for how long a task takes a human, doubling its lifecycle cost cuts an AI agent's effective time horizon roughly in half"}


def check(ctx):
    return ctx.require('metr', r'controlling for how long these tasks would take humans', r'doubling of lifecycle cost.*roughly equivalent to halving the time horizon')


if __name__ == '__main__':
    run_cli(CLAIM, check)
