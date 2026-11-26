import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e72-dinner-table-speed', 'artifact': 'episode', 'type': 'comparison', 'story': 'Disclosure divide', 'quote': 'at dinner-table speed'}


def check(ctx):
    return ctx.need(None, None, 'Metaphorical cadence; no dinner timeline supplied.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
