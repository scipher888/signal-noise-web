import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e71-blocker-comparison', 'artifact': 'episode', 'type': 'comparison', 'story': 'Alignment evaluations', 'quote': "In OpenAI's own alignment evaluations, 6.2 models were also more likely in two tests to omit mentioning missing files or unavailable tools that blocked their work"}


def check(ctx):
    return ctx.require('gpt', r'Both models performed similarly to GPT-6 Astra on most alignment evaluations', r'in two tests, they were more likely to omit mentioning obstacles that blocked their work, such as a missing file or unavailable search tool')


if __name__ == '__main__':
    run_cli(CLAIM, check)
