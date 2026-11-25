import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't22-folding-gap', 'artifact': 'takeaways', 'type': 'comparison', 'story': 'GPT-6 protein binders', 'quote': "even OpenAI's latest internal model scores under 0.4 on whole-protein folding versus 0.93 for ESMFold2"}


def check(ctx):
    return ctx.require('openai', r'Across the full test, the average score rose from.*0\.38 for our latest internal model', r'ESMFold2 averaged 0\.93.*predict a whole protein.s structure from its sequence alone')


if __name__ == '__main__':
    run_cli(CLAIM, check)
