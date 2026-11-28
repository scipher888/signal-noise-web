import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e61-feedback-tone', 'artifact': 'episode', 'type': 'opinion', 'story': 'Astra feedback', 'quote': 'Early practitioner feedback, however, has been blunt'}


def check(ctx):
    return ctx.need('thezvi', ctx.find('thezvi', r'feedback on Astra has mostly been negative'), 'Blunt describes tone; this is a selection of reactions.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
