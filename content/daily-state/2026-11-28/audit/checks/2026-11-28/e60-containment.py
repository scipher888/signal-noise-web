import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e60-containment', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Astra risk rating', 'quote': 'paired with new internal containment controls'}


def check(ctx):
    return ctx.require('gpt', r'strengthened containment in our research environments', r'built Control Room.*can halt further model output')


if __name__ == '__main__':
    run_cli(CLAIM, check)
