import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e43-0586', 'artifact': 'episode', 'type': 'comparison', 'story': 'Blueprint', 'quote': 'edging past the human baseline of 0.586'}


def check(ctx):
    return ctx.require('blueprint', r'Human\* 0\.586')


if __name__ == '__main__':
    run_cli(CLAIM, check)
