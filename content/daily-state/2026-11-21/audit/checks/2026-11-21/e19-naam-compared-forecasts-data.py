import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e19-naam-compared-forecasts-data', 'artifact': 'episode', 'type': 'attribution', 'story': 'AI task-horizon analysis', 'quote': 'Naam compared famous task-horizon forecasts, like METR extrapolations and the original AI 2027 scenario, against actual internal usage data released by OpenAI and Google DeepMind'}


def check(ctx):
    return ctx.require('naam', r'OpenAI and Google', r'original AI 2027 scenario', r'Google DeepMind', r'METR')


if __name__ == '__main__':
    run_cli(CLAIM, check)
