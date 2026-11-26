import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't01-google-posted', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Gemini math papers', 'quote': 'Google Research posted six Gemini 4 math papers'}


def check(ctx):
    return ctx.require('framing', r'Google Research posts six Cogentic papers, produced with Gemini 4')


if __name__ == '__main__':
    run_cli(CLAIM, check)
