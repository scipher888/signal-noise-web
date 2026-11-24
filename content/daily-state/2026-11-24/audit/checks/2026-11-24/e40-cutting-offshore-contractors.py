import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e40-cutting-offshore-contractors', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Anthropic Enterprise Study', 'quote': 'many are cutting offshore contractors'}


def check(ctx):
    return ctx.require('anthropic', r'Many also reported reducing their use of contractors, particularly offshore ones')


if __name__ == '__main__':
    run_cli(CLAIM, check)
