import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's12-naam-compared-forecasts', 'artifact': 'short', 'type': 'attribution', 'story': 'AI Autonomous Horizons', 'quote': 'Ramez Naam compared famous AI forecasts against internal Google and OpenAI data'}


def check(ctx):
    return ctx.require('naam', r'Ramez Naam', r'Real world data from OpenAI and Google.*METR, AI 2027')


if __name__ == '__main__':
    run_cli(CLAIM, check)
