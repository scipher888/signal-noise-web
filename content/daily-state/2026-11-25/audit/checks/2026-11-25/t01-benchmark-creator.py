import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't01-benchmark-creator', 'artifact': 'takeaways', 'type': 'attribution', 'story': "Humanity's First Exam", 'quote': "Google DeepMind's new Humanity's First Exam benchmark"}


def check(ctx):
    return ctx.require('kaggle', r'Today, @GoogleDeepMind is launching Humanity.s First Exam on Kaggle, a benchmark')


if __name__ == '__main__':
    run_cli(CLAIM, check)
