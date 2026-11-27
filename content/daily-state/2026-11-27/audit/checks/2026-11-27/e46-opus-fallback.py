import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e46-opus-fallback', 'artifact': 'episode', 'type': 'attribution', 'story': 'Anthropic capability limits', 'quote': 'narrow topics fall back visibly to Opus 5'}


def check(ctx):
    return ctx.require('claude', r'For a small set of topics, the models fall back transparently to Opus 5\b')


if __name__ == '__main__':
    run_cli(CLAIM, check)
