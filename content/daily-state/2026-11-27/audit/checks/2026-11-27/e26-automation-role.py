import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e26-automation-role', 'artifact': 'episode', 'type': 'opinion', 'story': 'Sources of acceleration', 'quote': 'Even the role of AI automation is hard to isolate.'}


def check(ctx):
    return ctx.need('metr', ctx.find('metr', r'Lower pretraining loss could be attributable to a number of factors'), 'Interpretation of confounding.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
