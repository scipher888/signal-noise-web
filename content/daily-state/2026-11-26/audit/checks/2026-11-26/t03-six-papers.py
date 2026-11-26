import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't03-six-papers', 'artifact': 'takeaways', 'type': 'number', 'story': 'Cogentic papers', 'quote': 'six new math papers'}


def check(ctx):
    return ctx.require('framing', r'Google Research posts six Cogentic papers, produced with Gemini 4, claiming results on factoring, the log-rank conjecture', note='New postings; does not certify novelty or correctness of results.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
