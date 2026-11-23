import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e04-150-year-old-millennium', 'artifact': 'episode', 'type': 'number', 'story': 'Riemann Hypothesis proof', 'quote': 'a one-hundred-and-fifty-year-old Millennium Prize problem'}


def check(ctx):
    s1 = ctx.find('alpoge', r'150 years')
    s2 = ctx.find('artificialanlys', r'Millennium Prize Problems')
    if s1 and s2:
        return ctx.ok('alpoge', s1, 'Millennium Prize status confirmed via artificialanlys')
    return ctx.need('alpoge', s1 or s2, 'Could not verify both 150-year age and Millennium Prize status')


if __name__ == '__main__':
    run_cli(CLAIM, check)
