import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e60-refused-to-name', 'artifact': 'episode', 'type': 'attribution', 'story': 'Aaronson crypto warning', 'quote': 'He deliberately refused to name RSA or claim anyone had factored large numbers in polynomial time'}


def check(ctx):
    return ctx.support_or_contradict('framing', r'(?=.*explicitly decline)(?=.*name RSA)(?=.*(?:polynomial.time factoring|factor .*polynomial time))', r'he explicitly declines to vouch for the specifics', 'Declining to vouch for specifics is not a statement that he refused to name RSA.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
