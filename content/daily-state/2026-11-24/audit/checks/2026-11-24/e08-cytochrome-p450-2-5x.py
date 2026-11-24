import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e08-cytochrome-p450-2-5x', 'artifact': 'episode', 'type': 'number', 'story': 'Quantum Circuits', 'quote': 'two and a half times for Cytochrome P450'}


def check(ctx):
    return ctx.require('deepmind', r'Cytochrome P450.*2\.5× improvement')


if __name__ == '__main__':
    run_cli(CLAIM, check)
