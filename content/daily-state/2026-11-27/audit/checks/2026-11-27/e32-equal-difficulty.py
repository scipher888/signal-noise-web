import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e32-equal-difficulty', 'artifact': 'episode', 'type': 'comparison', 'story': 'AI acceleration boundary', 'quote': 'If independent evaluators cannot cleanly separate frontier AI acceleration from ordinary engineering in a chart, labs are finding it just as hard to isolate inside a deployed model.'}


def check(ctx):
    return ctx.need('claude', ctx.find('claude', r'where the limits actually stop'), 'No common measure of difficulty in the two settings.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
