import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e18-task-duration', 'artifact': 'episode', 'type': 'number', 'story': "Humanity's First Exam", 'quote': 'ninety-second tasks'}


def check(ctx):
    return ctx.support_or_contradict('deepmind', r'each task (?:takes|lasts) 90 seconds', r'median solve time 1\.5 minutes, IQR 1\.0 to 2\.5 minutes', 'The reported 90 seconds is a median for seed prompts.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
