import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e23-nearly-half', 'artifact': 'episode', 'type': 'number', 'story': 'Society', 'quote': 'overturning the headline conclusion in nearly half of major-objection cases'}


def check(ctx):
    s = ctx.find('society', r'major objections, the scripts overturned the headline conclusion in (\d+) of (\d+)')
    if not s: return ctx.need('society', None, 'figure not found')
    n, d = map(int, re.search(r'in (\d+) of (\d+)', s).groups())
    return ctx.ok('society', s, f'{n}/{d} = {n/d:.1%}; "nearly half" holds') if 0.40 <= n / d < 0.5 else ctx.fail('society', s, f'{n}/{d} = {n/d:.1%} is not "nearly half"')


if __name__ == '__main__':
    run_cli(CLAIM, check)
