import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e19-task-examples', 'artifact': 'episode', 'type': 'qualifier', 'story': "Humanity's First Exam", 'quote': 'like counting objects, tracking arrows, or spotting a false premise'}


def check(ctx):
    return ctx.require('deepmind', r'visual object counting.*false-premise verification', r'Arrows/Pointers')


if __name__ == '__main__':
    run_cli(CLAIM, check)
