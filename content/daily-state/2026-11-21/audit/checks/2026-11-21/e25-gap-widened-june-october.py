import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e25-gap-widened-june-october', 'artifact': 'episode', 'type': 'comparison', 'story': 'AI task-horizon analysis', 'quote': 'the gap actually widened between June and October'}


def check(ctx):
    return ctx.require('naam', r'grew dramatically from June to October')


if __name__ == '__main__':
    run_cli(CLAIM, check)
