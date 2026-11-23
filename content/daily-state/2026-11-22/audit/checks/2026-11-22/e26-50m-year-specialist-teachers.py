import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e26-50m-year-specialist-teachers', 'artifact': 'episode', 'type': 'number', 'story': 'Nathan Lambert Cornell talk', 'quote': 'Frontier labs are spending 50 million dollars a year or more training specialist teachers and distilling them into single models'}


def check(ctx):
    return ctx.require('lambert', r'O\(\$50M\+/yr\)', r'train domain-specialist teachers.*single student')


if __name__ == '__main__':
    run_cli(CLAIM, check)
