import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't09-66-interviews', 'artifact': 'takeaways', 'type': 'number', 'story': 'Anthropic customer study', 'quote': '66 interviews'}


def check(ctx):
    return ctx.require('anthropic', r'66 interviews')


if __name__ == '__main__':
    run_cli(CLAIM, check)
