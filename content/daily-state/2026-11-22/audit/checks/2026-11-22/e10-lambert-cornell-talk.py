import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e10-lambert-cornell-talk', 'artifact': 'episode', 'type': 'attribution', 'story': 'Nathan Lambert Cornell talk', 'quote': "Nathan Lambert's talk at Cornell on the future of post-training"}


def check(ctx):
    return ctx.require('lambert', r'Nathan Lambert', r'Cornell University', r'Post-Training')


if __name__ == '__main__':
    run_cli(CLAIM, check)
