import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't15-frontier-labs', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'RSA rumors', 'quote': 'frontier labs'}


def check(ctx):
    return ctx.require('kimmonismus', r'OpenAI or Anthropic may have found a way to factor large numbers', note='Identifies the labs in the rumor, not a confirmed result.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
