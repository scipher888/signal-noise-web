import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't11-benchmark-gap', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Pretraining loss', 'quote': 'unmatched benchmark gains'}


def check(ctx):
    return ctx.require('metr', r'lack of a comparable acceleration in benchmark scores of OpenAI.s models')


if __name__ == '__main__':
    run_cli(CLAIM, check)
