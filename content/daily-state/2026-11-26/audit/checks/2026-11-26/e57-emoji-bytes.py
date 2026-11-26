import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e57-emoji-bytes', 'artifact': 'episode', 'type': 'comparison', 'story': 'Production verification', 'quote': 'Python escaping emojis in JSON tool calls while Rust wrote them raw'}


def check(ctx):
    return ctx.require('anthropic', r'when Python writes JSON tool calls, it escapes certain characters', r'an emoji\) by replacing them with text codes', r'Rust wrote those characters as is')


if __name__ == '__main__':
    run_cli(CLAIM, check)
