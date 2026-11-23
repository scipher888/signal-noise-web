import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't08-ant-self-reported-results', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Ant Group LingSante-3.1-flash', 'quote': "Ant Group's self-reported results claim"}


def check(ctx):
    return ctx.require('antlingagi', r'benchmark numbers are self-reported')


if __name__ == '__main__':
    run_cli(CLAIM, check)
