import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e25-random-null', 'artifact': 'episode', 'type': 'comparison', 'story': 'Society', 'quote': 'statistically indistinguishable from randomly citing recent papers'}


def check(ctx):
    s = ctx.find('society', r'recency-matched random citation null averaged [\d.]+ steps \(P = ([\d.]+)\)')
    if not s: return ctx.need('society', None, 'null comparison not found')
    p = float(re.search(r'P = ([\d.]+)', s).group(1))
    return ctx.ok('society', s, f'P = {p} > 0.05') if p > 0.05 else ctx.fail('society', s, f'P = {p} is significant')


if __name__ == '__main__':
    run_cli(CLAIM, check)
