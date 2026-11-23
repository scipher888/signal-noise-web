import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't12-number-theorist-guided-model', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Riemann Hypothesis Lean proof', 'quote': 'a world-class number theorist guided the model'}


def check(ctx):
    q = ctx.find('emollick', r'great mathematicians.*models can.t \(yet\) do it on their own')
    if ctx.find('emollick', r'number theorist'):
        return ctx.ok('emollick', q)
    return ctx.need('emollick', q, 'emollick says great mathematicians and models cannot do it on their own, without specifically saying number theorist guided the model')


if __name__ == '__main__':
    run_cli(CLAIM, check)
