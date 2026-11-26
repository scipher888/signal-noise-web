import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e40-six-produced', 'artifact': 'episode', 'type': 'number', 'story': 'Google papers', 'quote': 'produced all six'}


def check(ctx):
    return ctx.require('framing', r'Google Research posts six Cogentic papers, produced with Gemini 4', note='Reported scope of production, not independent validation.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
