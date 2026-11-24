import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't01-deepmind-reports-cheaper-circuits', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Google DeepMind quantum circuits', 'quote': 'Google DeepMind reports Gemini 4 agent teams found cheaper quantum circuits'}


def check(ctx):
    return ctx.require('deepmind', r'Google DeepMind', r'teams of Gemini 4 agents.*quantum circuits')


if __name__ == '__main__':
    run_cli(CLAIM, check)
