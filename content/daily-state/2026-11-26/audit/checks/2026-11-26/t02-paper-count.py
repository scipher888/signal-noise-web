import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't02-paper-count', 'artifact': 'takeaways', 'type': 'number', 'story': 'Gemini math papers', 'quote': 'six Gemini 4 math papers'}


def check(ctx):
    return ctx.require('framing', r'six Cogentic papers, produced with Gemini 4, claiming results on factoring, the log-rank conjecture')


if __name__ == '__main__':
    run_cli(CLAIM, check)
