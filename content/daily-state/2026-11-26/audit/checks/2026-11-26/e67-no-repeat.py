import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e67-no-repeat', 'artifact': 'episode', 'type': 'number', 'story': 'Engineering oversight', 'quote': "teams didn't have to catch the same shortcut twice"}


def check(ctx):
    return ctx.require('anthropic', r'engineer turned down the web search shortcut', r'Agents checked the memory note, recognized the known bug, and linked those records to it, instead of writing another workaround', note='Observed for this shortcut; not a zero-recurrence statistic across all shortcuts.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
