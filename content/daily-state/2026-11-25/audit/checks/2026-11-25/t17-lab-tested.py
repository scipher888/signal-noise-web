import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't17-lab-tested', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'GPT-6 protein binders', 'quote': 'lab-tested candidates'}


def check(ctx):
    return ctx.require('openai', r'We tested 322 minibinders against 5 targets in the lab')


if __name__ == '__main__':
    run_cli(CLAIM, check)
