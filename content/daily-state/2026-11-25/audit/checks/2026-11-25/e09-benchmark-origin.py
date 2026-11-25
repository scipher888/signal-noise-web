import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e09-benchmark-origin', 'artifact': 'episode', 'type': 'attribution', 'story': "Humanity's First Exam", 'quote': 'a new reliability benchmark from Google DeepMind'}


def check(ctx):
    return ctx.require('kaggle', r'@GoogleDeepMind is launching Humanity.s First Exam on Kaggle, a benchmark designed to measure .floor reliability')


if __name__ == '__main__':
    run_cli(CLAIM, check)
