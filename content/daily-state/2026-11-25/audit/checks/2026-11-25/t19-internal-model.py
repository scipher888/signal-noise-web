import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't19-internal-model', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'GPT-6 protein binders', 'quote': "OpenAI's latest internal model"}


def check(ctx):
    return ctx.require('openai', r'Across the full test, the average score rose from.*0\.38 for our latest internal model')


if __name__ == '__main__':
    run_cli(CLAIM, check)
