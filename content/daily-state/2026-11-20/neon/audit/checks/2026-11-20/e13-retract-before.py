import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e13-retract-before', 'artifact': 'episode', 'type': 'attribution', 'story': 'Society', 'quote': 'retracted mistakes publicly before upload'}


def check(ctx):
    return ctx.support_or_contradict('society', r'publicly retract mistaken claims before publication', r'correction preceded upload', 'retraction timing')


if __name__ == '__main__':
    run_cli(CLAIM, check)
