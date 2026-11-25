import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't03-kaggle-host', 'artifact': 'takeaways', 'type': 'qualifier', 'story': "Humanity's First Exam", 'quote': "Humanity's First Exam benchmark on Kaggle"}


def check(ctx):
    return ctx.require('kaggle', r'launching Humanity.s First Exam on Kaggle, a benchmark')


if __name__ == '__main__':
    run_cli(CLAIM, check)
