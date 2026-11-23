import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't06-hard-to-compare-across-labs', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'OpenAI perplexity warning', 'quote': 'perplexity is hard to compare across labs'}


def check(ctx):
    return ctx.require('openai', r'Difficulty of comparison across labs')


if __name__ == '__main__':
    run_cli(CLAIM, check)
