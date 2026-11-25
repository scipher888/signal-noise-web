import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e20-floor-definition', 'artifact': 'episode', 'type': 'qualifier', 'story': "Humanity's First Exam", 'quote': 'it measures floor reliability, asking whether a model solves four slightly varied versions of a task consistently across repeated tries'}


def check(ctx):
    return ctx.require('deepmind', r'routine task every time across repeated draws and controlled prompt variations', r'each four-prompt family pairs one seed prompt with three controlled variants')


if __name__ == '__main__':
    run_cli(CLAIM, check)
