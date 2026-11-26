import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e49-deterministic-factoring', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Google factoring', 'quote': 'the other achieves deterministic subexponential factoring without randomness'}


def check(ctx):
    return ctx.support_or_contradict('framing', r'(?=.*(?:other|second))(?=.*deterministic)(?=.*subexponential)(?=.*factor)', r'Company-posted claim; the running-time bound is subexponential', 'Only a claimed runtime is given, not a verified second deterministic algorithm.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
