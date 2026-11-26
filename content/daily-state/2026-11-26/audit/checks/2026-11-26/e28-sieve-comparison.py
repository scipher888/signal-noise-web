import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e28-sieve-comparison', 'artifact': 'episode', 'type': 'comparison', 'story': 'Google papers', 'quote': 'whose bounds do not beat the classic heuristic Number Field Sieve in practice'}


def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'running-time bound is subexponential, not polynomial'), 'This does not compare the bounds or practical performance to the Number Field Sieve.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
