import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e04-ant-released-lingsante', 'artifact': 'episode', 'type': 'attribution', 'story': 'Ant Group LingSante', 'quote': 'Ant Group released an open-weight medical model called LingSante-3.1-flash'}


def check(ctx):
    s1 = ctx.find('antlingagi', r'release LingSante-3\.1-flash, an open-weight')
    s2 = ctx.find('lingsante', r'LingSante-3\.1-flash is an open-weight.*medical')
    if s1 and s2:
        return ctx.ok('antlingagi', s1, 'Confirmed release of open-weight medical model LingSante-3.1-flash')
    return ctx.need('antlingagi', s1 or s2, 'Could not match release and medical open-weight description')


if __name__ == '__main__':
    run_cli(CLAIM, check)
