import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't05-proved-in-lean', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Google DeepMind quantum circuits', 'quote': 'every circuit was mathematically proved in Lean'}


def check(ctx):
    return ctx.require('deepmind', r'proved each result using Lean')


if __name__ == '__main__':
    run_cli(CLAIM, check)
