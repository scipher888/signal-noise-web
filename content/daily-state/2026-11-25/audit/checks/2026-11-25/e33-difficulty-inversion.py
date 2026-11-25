import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e33-difficulty-inversion', 'artifact': 'episode', 'type': 'comparison', 'story': "Humanity's First Exam", 'quote': 'Human and AI difficulty are literally inverted: people handle vision easily and trip over formal logic, while models do the reverse'}


def check(ctx):
    return ctx.require('deepmind', r'humans score highest on Vision \(84%\).*lowest at the subcategory level on Logical Deduction \(59\.4%\), whereas models invert that order')


if __name__ == '__main__':
    run_cli(CLAIM, check)
