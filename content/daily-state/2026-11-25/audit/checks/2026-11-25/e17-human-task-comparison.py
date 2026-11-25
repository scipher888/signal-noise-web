import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e17-human-task-comparison', 'artifact': 'episode', 'type': 'comparison', 'story': "Humanity's First Exam", 'quote': 'Instead of PhD-level questions, it tests simple, ninety-second tasks humans breeze through'}


def check(ctx):
    q = ctx.find('deepmind', r'median solve time 1\.5 minutes, IQR 1\.0 to 2\.5 minutes')
    return ctx.fail('deepmind', q, 'Ninety seconds is the median human seed solve time, not a duration specified for the tasks.') if q else ctx.need('deepmind', None, 'Verify timing and population.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
