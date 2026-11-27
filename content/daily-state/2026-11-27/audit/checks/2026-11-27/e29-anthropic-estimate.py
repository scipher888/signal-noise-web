import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e29-anthropic-estimate', 'artifact': 'episode', 'type': 'attribution', 'story': 'Sources of acceleration', 'quote': "METR has separately estimated that a majority of Anthropic's own recent acceleration comes from AI"}


def check(ctx):
    return ctx.require('metr', r'METR.s recent assessment.*at Anthropic.*estimated that .a majority \(perhaps ≈80%\) of the current \(October 2026\) acceleration is due to AI')


if __name__ == '__main__':
    run_cli(CLAIM, check)
