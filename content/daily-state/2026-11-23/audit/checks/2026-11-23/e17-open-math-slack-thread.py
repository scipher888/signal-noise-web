import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e17-open-math-slack-thread', 'artifact': 'episode', 'type': 'attribution', 'story': 'OpenAI Perplexity', 'quote': 'Pachocki says it began solving open mathematics problems one after another in a single Slack thread'}


def check(ctx):
    return ctx.require('openai', r'open problems in mathematics', r'one after another in a single Slack thread')


if __name__ == '__main__':
    run_cli(CLAIM, check)
