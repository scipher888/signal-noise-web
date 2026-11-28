import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e51-first-perfect', 'artifact': 'episode', 'type': 'comparison', 'story': 'Astra benchmarks', 'quote': 'the first model to score 100 percent on ARC-AGI-3'}


def check(ctx):
    return ctx.require('thezvi', r'GPT-6\.2 Astra is the first model to achieve a 100% score on ARC-AGI-3')


if __name__ == '__main__':
    run_cli(CLAIM, check)
