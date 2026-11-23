import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't09-560b-open-weight-lingsante', 'artifact': 'takeaways', 'type': 'number', 'story': 'Ant Group LingSante-3.1-flash', 'quote': '560B open-weight LingSante-3.1-flash'}


def check(ctx):
    return ctx.require('antlingagi', r'LingSante-3\.1-flash, an open-weight MoE model with 560B total parameters')


if __name__ == '__main__':
    run_cli(CLAIM, check)
