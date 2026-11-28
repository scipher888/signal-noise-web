import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e08-tangible', 'artifact': 'episode', 'type': 'opinion', 'story': 'App control risks', 'quote': 'Handing models live controls inside real applications makes capability gains immediately tangible'}


def check(ctx):
    return ctx.need('unslothai', ctx.find('unslothai', r'successfully controlled those apps'), 'The demo is evidence of app use; tangibility is an editorial judgment.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
