import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e16-end-dates', 'artifact': 'episode', 'type': 'qualifier', 'story': 'METR chart debate', 'quote': 'missing pretraining end dates'}


def check(ctx):
    return ctx.require('metr', r'The rough date that the pretraining run ended for each model', r'Plotting models at their public release dates may not capture when pretraining progress happened')


if __name__ == '__main__':
    run_cli(CLAIM, check)
