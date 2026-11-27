import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e63-clean-border', 'artifact': 'episode', 'type': 'opinion', 'story': 'AI acceleration boundary', 'quote': 'Right now, neither evaluators nor labs can draw that border cleanly'}


def check(ctx):
    return ctx.need('metr', ctx.find('metr', r'knowing the lag helps us determine how much AI uplift'), 'Cross-story editorial conclusion.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
