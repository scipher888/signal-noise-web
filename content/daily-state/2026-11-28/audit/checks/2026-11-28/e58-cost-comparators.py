import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e58-cost-comparators', 'artifact': 'episode', 'type': 'comparison', 'story': 'Astra benchmarks', 'quote': 'at sharply lower cost per task'}


def check(ctx):
    return ctx.require('gpt', r'Astra scores 9 percentage points higher than GPT-6 Astra at less than one-third the cost', r'doubling Claude Fable 5\.2.s pass rate at about one-sixth the cost', note='Different reference models on the science and legal tests.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
