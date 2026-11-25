import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't07-simple-tasks', 'artifact': 'takeaways', 'type': 'qualifier', 'story': "Humanity's First Exam", 'quote': 'simple tasks'}


def check(ctx):
    return ctx.require('deepmind', r'simple text and image tasks humans get right almost every time')


if __name__ == '__main__':
    run_cli(CLAIM, check)
