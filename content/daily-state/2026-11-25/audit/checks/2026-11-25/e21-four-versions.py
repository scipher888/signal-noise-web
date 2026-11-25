import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e21-four-versions', 'artifact': 'episode', 'type': 'number', 'story': "Humanity's First Exam", 'quote': 'four slightly varied versions of a task'}


def check(ctx):
    return ctx.require('deepmind', r'each four-prompt family pairs one seed prompt with three controlled variants')


if __name__ == '__main__':
    run_cli(CLAIM, check)
