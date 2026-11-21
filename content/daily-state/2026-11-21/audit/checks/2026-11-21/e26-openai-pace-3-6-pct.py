import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e26-openai-pace-3-6-pct', 'artifact': 'episode', 'type': 'number', 'story': 'AI task-horizon analysis', 'quote': "OpenAI's pace of research experiments is rising only about three point six percent per point of capability gain"}


def check(ctx):
    return ctx.require('naam', r'3\.6% faster experimentation per point of ECI')


if __name__ == '__main__':
    run_cli(CLAIM, check)
