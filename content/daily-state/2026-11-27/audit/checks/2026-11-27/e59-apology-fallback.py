import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e59-apology-fallback', 'artifact': 'episode', 'type': 'attribution', 'story': 'June fallback change', 'quote': 'before apologizing and switching to visible fallbacks'}


def check(ctx):
    return ctx.require('claude', r'Anthropic apologized and reversed course within days', r'Within days, the invisible limits were replaced with a visible fallback')


if __name__ == '__main__':
    run_cli(CLAIM, check)
