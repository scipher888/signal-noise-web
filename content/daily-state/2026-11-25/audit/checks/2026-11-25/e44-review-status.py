import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e44-review-status', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Protein design', 'quote': "OpenAI's own unreviewed preprint"}


def check(ctx):
    return ctx.require('framing', r'framing \(OpenAI\): Company-reported preprint', note='Preprint status of the reported version; not an independent reviewed result.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
