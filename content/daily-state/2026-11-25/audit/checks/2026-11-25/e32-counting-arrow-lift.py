import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e32-counting-arrow-lift', 'artifact': 'episode', 'type': 'number', 'story': "Humanity's First Exam", 'quote': 'improves object counting and arrow tracking by barely 2 points'}


def check(ctx):
    return ctx.require('deepmind', r'\+2\.0 percentage points on Arrows/Pointers and \+1\.9 percentage points on Object Counting')


if __name__ == '__main__':
    run_cli(CLAIM, check)
