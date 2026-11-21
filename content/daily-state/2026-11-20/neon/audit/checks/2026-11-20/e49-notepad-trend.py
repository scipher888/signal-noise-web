import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e49-notepad-trend', 'artifact': 'episode', 'type': 'number', 'story': 'Blueprint', 'quote': 'general frontier models given a persistent notepad to carry lessons across apartments are climbing steadily at four-hundredths of a point per month'}


def check(ctx):
    # Is +0.04/month a notepad effect? Source: a trend line over SOTA models by release date.
    return ctx.support_or_contradict('blueprint', r'notepad[^.]{0,120}0\.04|0\.04[^.]{0,120}notepad',
        r'SOTA frontier models are labeled and a trend line is fitted .* \+0\.04/month',
        '+0.04/month is the trend of SOTA scores against model release date, not models improving via the notepad')


if __name__ == '__main__':
    run_cli(CLAIM, check)
