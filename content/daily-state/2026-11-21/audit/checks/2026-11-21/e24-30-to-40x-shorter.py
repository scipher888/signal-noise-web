import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e24-30-to-40x-shorter', 'artifact': 'episode', 'type': 'comparison', 'story': 'AI task-horizon analysis', 'quote': 'thirty to forty times shorter than the benchmark extrapolations'}


def check(ctx):
    return ctx.require('naam', r'33× OpenAI.*41× Google')


if __name__ == '__main__':
    run_cli(CLAIM, check)
