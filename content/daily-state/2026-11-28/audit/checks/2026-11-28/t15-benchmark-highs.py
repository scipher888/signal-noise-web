import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't15-benchmark-highs', 'artifact': 'takeaways', 'type': 'comparison', 'story': 'Benchmarks and builder reports', 'quote': 'benchmark highs'}


def check(ctx):
    return ctx.require('gpt', r'new high on Terminal-Bench-Science', r'new high on the Vals Science Index')


if __name__ == '__main__':
    run_cli(CLAIM, check)
