import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's15-trail-forecasts-30-40x', 'artifact': 'short', 'type': 'comparison', 'story': 'AI Autonomous Horizons', 'quote': 'Real Horizons Trail Forecasts by 30–40x'}


def check(ctx):
    return ctx.require('naam', r'33× OpenAI.*41× Google')


if __name__ == '__main__':
    run_cli(CLAIM, check)
