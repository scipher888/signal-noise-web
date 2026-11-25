import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't09-consistency-scope', 'artifact': 'takeaways', 'type': 'qualifier', 'story': "Humanity's First Exam", 'quote': 'when required to be consistent across four variations'}


def check(ctx):
    return ctx.support_or_contradict('deepmind', r'Family pass⁴ measures the unbiased joint probability that all 4 (?:family members|variations|prompts) succeed(?: with one draw each)?', r'Family pass⁴ measures the unbiased joint probability that all 16 draws \(4 per prompt across all 4 family members\) succeed', 'Family pass^4 is consistency across 16 draws (4 per prompt x 4 family members), not only across four variations.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
