import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e39-self-reported', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Ant Group LingSante', 'quote': 'They are self-reported'}


def check(ctx):
    return ctx.require('antlingagi', r'benchmark numbers are self-reported')


if __name__ == '__main__':
    run_cli(CLAIM, check)
