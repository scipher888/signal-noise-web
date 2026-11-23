import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't04-2027-outrun-alignment', 'artifact': 'takeaways', 'type': 'number', 'story': 'OpenAI perplexity warning', 'quote': 'AI-driven pretraining breakthroughs could outrun alignment by 2027'}


def check(ctx):
    return ctx.require('openai', r'as soon as 2027.*avalanche of fundamental pretraining advancements', r'progress on alignment and monitoring.*unlikely to be fast enough')


if __name__ == '__main__':
    run_cli(CLAIM, check)
