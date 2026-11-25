import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e41-second-experiment', 'artifact': 'episode', 'type': 'number', 'story': 'Protein design', 'quote': 'In a second lab run'}


def check(ctx):
    return ctx.require('openai', r'Laboratory Experiment 2: Designing new sequences for 3D protein structures', r'We tested whether GPT.6\.2 could design the sequences itself')


if __name__ == '__main__':
    run_cli(CLAIM, check)
