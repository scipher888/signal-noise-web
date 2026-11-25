import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e31-symbolic-lift', 'artifact': 'episode', 'type': 'number', 'story': "Humanity's First Exam", 'quote': 'Cranking up reasoning effort lifts symbolic logic by nearly 30 percentage points'}


def check(ctx):
    return ctx.require('deepmind', r'Raising effort from low to high.*symbolic text subcategories \(\+26\.2 to \+29\.7 percentage points mean lift on Logical Deduction', note='Approximation for selected symbolic subcategories, not all reasoning.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
