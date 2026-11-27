import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e23-underlying-fog', 'artifact': 'episode', 'type': 'opinion', 'story': 'Sources of acceleration', 'quote': 'Once the presentation debate cleared, the underlying fog remained.'}


def check(ctx):
    return ctx.need('metr', ctx.find('metr', r'There remain substantial disagreements'), 'Editorial interpretation.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
