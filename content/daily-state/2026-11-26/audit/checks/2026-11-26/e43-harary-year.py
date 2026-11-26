import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e43-harary-year', 'artifact': 'episode', 'type': 'number', 'story': 'Google papers', 'quote': "Harary's 1964 graph reconstruction conjecture"}


def check(ctx):
    return ctx.require('framing', r'(?=.*Harary)(?=.*1964)(?=.*graph reconstruction conjecture)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
