import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e17-six-cogentic', 'artifact': 'episode', 'type': 'attribution', 'story': 'Google papers', 'quote': 'six papers produced by its Cogentic harness on Gemini 4'}


def check(ctx):
    return ctx.require('framing', r'Google Research posts six Cogentic papers, produced with Gemini 4')


if __name__ == '__main__':
    run_cli(CLAIM, check)
