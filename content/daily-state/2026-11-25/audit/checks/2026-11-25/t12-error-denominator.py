import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't12-error-denominator', 'artifact': 'takeaways', 'type': 'number', 'story': "Humanity's First Exam", 'quote': 'nearly three-quarters of errors coming from basic visual perception'}


def check(ctx):
    q = ctx.find('deepmind', r'Visual perception errors \(73% of wrong rollouts\)')
    return ctx.fail('deepmind', q, 'The measured denominator is wrong answers, not all errors including refusals, truncation and harness failures.') if q else ctx.need('deepmind', None, 'Verify denominator.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
