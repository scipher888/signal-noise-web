import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't14-preprint-status', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'GPT-6 protein binders', 'quote': 'unreviewed preprint'}


def check(ctx):
    return ctx.require('framing', r'Company-reported preprint with lab tests run by its research partner', note='Status of the cited version, not evidence of independent peer review.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
