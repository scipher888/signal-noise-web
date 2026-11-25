import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't20-folding-score', 'artifact': 'takeaways', 'type': 'number', 'story': 'GPT-6 protein binders', 'quote': 'scores under 0.4 on whole-protein folding'}


def check(ctx):
    return ctx.require('openai', r'average score rose from.*0\.38 for our latest internal model', r'predict a whole protein.s structure from its sequence alone')


if __name__ == '__main__':
    run_cli(CLAIM, check)
