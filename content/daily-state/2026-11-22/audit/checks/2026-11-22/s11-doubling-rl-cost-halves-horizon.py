import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's11-doubling-rl-cost-halves-horizon', 'artifact': 'short', 'type': 'comparison', 'story': 'AI Verification & Riemann Proof', 'quote': "doubling a task's cost to run as an RL environment cuts an agent's effective horizon roughly in half"}


def check(ctx):
    return ctx.require('metr', r'Lifecycle Cost.*RL training environment', r'doubling of lifecycle cost.*roughly equivalent to halving the time horizon')


if __name__ == '__main__':
    run_cli(CLAIM, check)
