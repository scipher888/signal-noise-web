import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e43-cap-level', 'artifact': 'episode', 'type': 'comparison', 'story': 'Anthropic capability limits', 'quote': "near Opus 5.5's level"}


def check(ctx):
    return ctx.require('claude', r'both models perform .at about the level of Opus 5\.5')


if __name__ == '__main__':
    run_cli(CLAIM, check)
