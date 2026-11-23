import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't05-proposes-industry-limits', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'OpenAI perplexity warning', 'quote': 'proposes industry limits until safety monitoring milestones are met'}


def check(ctx):
    return ctx.require('openai', r'propose common limits.*not crossing until.*monitor AI behavior achieves a certain concrete milestone')


if __name__ == '__main__':
    run_cli(CLAIM, check)
