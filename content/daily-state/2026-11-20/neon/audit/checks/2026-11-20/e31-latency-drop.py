import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e31-latency-drop', 'artifact': 'episode', 'type': 'number', 'story': 'Airbnb', 'quote': 'median latency dropped from roughly 900 milliseconds to 35'}


def check(ctx):
    # "dropped from 900 to 35" implies one system got faster; sources compare two different models.
    return ctx.support_or_contradict('gemma', r'(drop|fell|reduc|cut)\w*[^.]{0,40}900', r'35ms median latency \(85ms p99\) vs\. ~900ms for frontier models',
        'not a drop: 35 ms is the fine-tuned Gemma, ~900 ms is the frontier models')


if __name__ == '__main__':
    run_cli(CLAIM, check)
