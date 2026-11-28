import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e57-science-law-highs', 'artifact': 'episode', 'type': 'comparison', 'story': 'Astra benchmarks', 'quote': 'leads science and legal evaluations'}


def check(ctx):
    return ctx.require('gpt', r'new high on Terminal-Bench-Science', r'Harvey LAB[-‑]AA.*legal assignments', r'Astra sets a new state of the art, more than doubling Claude Fable 5\.2.s pass rate')


if __name__ == '__main__':
    run_cli(CLAIM, check)
