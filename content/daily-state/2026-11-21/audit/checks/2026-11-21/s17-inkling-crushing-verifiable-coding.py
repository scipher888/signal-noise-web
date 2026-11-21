import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's17-inkling-crushing-verifiable-coding', 'artifact': 'short', 'type': 'comparison', 'story': 'Inkling 2 Mini', 'quote': "laptop models like Thinking Machines' new Inkling 2 Mini are already crushing verifiable coding benchmarks"}


def check(ctx):
    return ctx.require('thinking', r'small enough to run on your laptop', r'scores ahead of every comparable model on agentic coding benchmarks')


if __name__ == '__main__':
    run_cli(CLAIM, check)
