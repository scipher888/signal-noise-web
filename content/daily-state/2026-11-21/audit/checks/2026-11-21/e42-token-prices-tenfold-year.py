import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e42-token-prices-tenfold-year', 'artifact': 'episode', 'type': 'number', 'story': 'Arvind Narayanan warning', 'quote': 'driving token prices down tenfold a year'}


def check(ctx):
    s = ctx.find('random_walker', r'(?:tenfold|10x|token price|price)')
    if s:
        return ctx.ok('random_walker', s)
    return ctx.fail('random_walker', ctx.find('random_walker', r'sustainable businesses'), 'Source post by Arvind Narayanan does not mention driving token prices down tenfold a year')


if __name__ == '__main__':
    run_cli(CLAIM, check)
