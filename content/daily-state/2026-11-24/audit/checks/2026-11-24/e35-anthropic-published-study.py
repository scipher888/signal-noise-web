import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e35-anthropic-published-study', 'artifact': 'episode', 'type': 'attribution', 'story': 'Anthropic Enterprise Study', 'quote': 'Anthropic published a study'}


def check(ctx):
    return ctx.require('anthropic', r'Working with AI.*Anthropic', r'we conducted 66 interviews')


if __name__ == '__main__':
    run_cli(CLAIM, check)
