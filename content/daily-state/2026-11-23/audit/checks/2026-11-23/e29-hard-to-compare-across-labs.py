import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e29-hard-to-compare-across-labs', 'artifact': 'episode', 'type': 'comparison', 'story': 'OpenAI Perplexity', 'quote': 'perplexity is notoriously hard to compare across labs'}


def check(ctx):
    return ctx.require('openai', r'Difficulty of comparison across labs')


if __name__ == '__main__':
    run_cli(CLAIM, check)
