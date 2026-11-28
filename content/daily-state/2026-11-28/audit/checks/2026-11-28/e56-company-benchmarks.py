import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e56-company-benchmarks', 'artifact': 'episode', 'type': 'attribution', 'story': 'Astra benchmarks', 'quote': 'OpenAI reports that Astra leads science and legal evaluations at sharply lower cost per task'}


def check(ctx):
    return ctx.require('gpt', r'new high on Terminal-Bench-Science', r'Astra scores 9 percentage points higher than GPT-6 Astra at less than one-third the cost', r'Harvey LAB. AA|Harvey LAB[-‑]AA.*legal assignments', r'Astra sets a new state of the art, more than doubling Claude Fable 5\.2.s pass rate at about one-sixth the cost')


if __name__ == '__main__':
    run_cli(CLAIM, check)
