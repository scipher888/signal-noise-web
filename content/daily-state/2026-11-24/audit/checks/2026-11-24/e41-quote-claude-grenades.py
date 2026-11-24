import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e41-quote-claude-grenades', 'artifact': 'episode', 'type': 'quote', 'story': 'Anthropic Enterprise Study', 'quote': 'what one interviewee called Claude grenades'}


def check(ctx):
    return ctx.require('anthropic', r'Claude grenades')


if __name__ == '__main__':
    run_cli(CLAIM, check)
