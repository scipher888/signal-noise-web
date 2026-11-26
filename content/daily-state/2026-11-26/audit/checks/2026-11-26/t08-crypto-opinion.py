import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't08-crypto-opinion', 'artifact': 'takeaways', 'type': 'opinion', 'story': 'Gemini math papers', 'quote': 'nothing of practical cryptographic relevance in their factoring results'}


def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'running-time bound is subexponential'), 'The asymptotic classification alone cannot decide practical relevance.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
