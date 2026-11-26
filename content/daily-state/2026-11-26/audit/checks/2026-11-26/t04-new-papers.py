import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't04-new-papers', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Cogentic papers', 'quote': 'new math papers'}


def check(ctx):
    return ctx.require('framing', r'posts six Cogentic papers, produced with Gemini 4, claiming results on factoring, the log-rank conjecture', note='Newly posted papers on mathematical topics.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
