import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't05-controlling-human-time', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'METR AI agent time horizon', 'quote': 'even after controlling for how long the task takes a human'}


def check(ctx):
    return ctx.require('metr', r'even after controlling for how long these tasks would take humans')


if __name__ == '__main__':
    run_cli(CLAIM, check)
