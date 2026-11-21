import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e40-text-remained-legible', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Inkling 2 Mini', 'quote': 'though at this scale the text remained legible'}


def check(ctx):
    return ctx.require('thinking', r'stayed legible throughout', r'at this scale we do not see a meaningful reduction in the monitorability')


if __name__ == '__main__':
    run_cli(CLAIM, check)
