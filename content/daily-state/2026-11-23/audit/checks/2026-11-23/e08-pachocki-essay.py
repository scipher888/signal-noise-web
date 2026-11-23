import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e08-pachocki-essay', 'artifact': 'episode', 'type': 'attribution', 'story': 'OpenAI Perplexity', 'quote': 'Chief Scientist Jakub Pachocki published an essay called Perplexity and Intelligence'}


def check(ctx):
    return ctx.require('openai', r'Perplexity and Intelligence', r'By Jakub Pachocki, Chief Scientist at OpenAI')


if __name__ == '__main__':
    run_cli(CLAIM, check)
