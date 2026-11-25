import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e39-binder-count', 'artifact': 'episode', 'type': 'number', 'story': 'Protein design', 'quote': "35 of 322 small protein binders based on GPT-6.2's shapes bound to their targets"}


def check(ctx):
    return ctx.require('openai', r'we made proteins based on GPT.6\.2.s designs and measured how strongly they bound', r'We tested 322 minibinders against 5 targets in the lab', r'Of those, 35 \(10\.9%\) tested positive for binding to their intended target')


if __name__ == '__main__':
    run_cli(CLAIM, check)
