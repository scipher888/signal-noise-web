import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't14-company-highs', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Benchmarks and builder reports', 'quote': 'OpenAI-reported benchmark highs'}


def check(ctx):
    return ctx.require('gpt', r'On Agents. Last Exam.*Astra sets a new high', r'new high on Terminal-Bench-Science')


if __name__ == '__main__':
    run_cli(CLAIM, check)
