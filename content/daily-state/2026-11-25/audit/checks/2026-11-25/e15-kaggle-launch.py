import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e15-kaggle-launch', 'artifact': 'episode', 'type': 'attribution', 'story': "Humanity's First Exam", 'quote': "Google DeepMind put hard numbers on that gap today, launching Humanity's First Exam on Google-owned Kaggle"}


def check(ctx):
    return ctx.require('kaggle', r'Today, @GoogleDeepMind is launching Humanity.s First Exam on Kaggle.*floor reliability', r'Kaggle is owned by Google', r'Top five models reach 96%–98% pass@1.*85\.6% on family pass\^4', note='Today refers to the announcement; the measured gap is between coverage and consistency.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
