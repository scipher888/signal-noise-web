import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e50-before-output', 'artifact': 'episode', 'type': 'qualifier', 'story': 'API refusal and fallback behavior', 'quote': 'still be billed before any output appears'}


def check(ctx):
    return ctx.require('framing', r'(?:refusal|request).*bill(?:ed|ing).*before any output', note='The supplied docs summary does not specify billing.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
