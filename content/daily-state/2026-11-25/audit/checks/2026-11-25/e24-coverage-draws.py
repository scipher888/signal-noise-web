import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e24-coverage-draws', 'artifact': 'episode', 'type': 'number', 'story': "Humanity's First Exam", 'quote': 'solve every task family at least once across four attempts'}


def check(ctx):
    return ctx.support_or_contradict('deepmind', r'Family pass@4 is the probability that at least 1 of 4 draws across a family succeeds', r'Family pass@4 is the probability that at least 1 of 16 draws across a family succeeds', 'The announced 100% is family coverage with four draws per prompt, not four attempts total per family.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
