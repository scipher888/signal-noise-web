import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't13-openai-report', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'GPT-6 protein binders', 'quote': 'In an unreviewed preprint, OpenAI reports'}


def check(ctx):
    return ctx.require('framing', r'framing \(OpenAI\): Company-reported preprint')


if __name__ == '__main__':
    run_cli(CLAIM, check)
