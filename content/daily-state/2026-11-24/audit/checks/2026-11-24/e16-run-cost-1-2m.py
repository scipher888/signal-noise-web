import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e16-run-cost-1-2m', 'artifact': 'episode', 'type': 'number', 'story': 'Linux Cybersecurity', 'quote': 'in a single run costing 1.2 million dollars in API credits'}


def check(ctx):
    return ctx.require('openai2', r'1\.2\s*million', r'API credits', note='Primary OpenAI research post not in snapshot; cost not in openai2')


if __name__ == '__main__':
    run_cli(CLAIM, check)
