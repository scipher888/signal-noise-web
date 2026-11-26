import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't23-refused-specific-claims', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'RSA rumors', 'quote': 'deliberately refused to name RSA or claim polynomial-time factoring'}


def check(ctx):
    return ctx.support_or_contradict('framing', r'(?=.*explicitly decline)(?=.*name RSA)(?=.*polynomial.time factoring)', r'he explicitly declines to vouch for the specifics', 'Not vouching is not the same as deliberately refusing to name RSA.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
