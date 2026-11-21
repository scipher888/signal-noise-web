import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e35-hundreds-thousands', 'artifact': 'episode', 'type': 'number', 'story': 'Airbnb', 'quote': 'fine-tuning on hundreds of thousands of labeled production examples'}


def check(ctx):
    return ctx.require('airbnb', r'hundreds of thousands of domain-specific examples')


if __name__ == '__main__':
    run_cli(CLAIM, check)
