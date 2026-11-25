import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't16-tested-hit-count', 'artifact': 'takeaways', 'type': 'number', 'story': 'GPT-6 protein binders', 'quote': '35 of 322 lab-tested candidates binding to their targets'}


def check(ctx):
    return ctx.require('openai', r'We tested 322 minibinders against 5 targets in the lab', r'Of those, 35 \(10\.9%\) tested positive for binding to their intended target')


if __name__ == '__main__':
    run_cli(CLAIM, check)
