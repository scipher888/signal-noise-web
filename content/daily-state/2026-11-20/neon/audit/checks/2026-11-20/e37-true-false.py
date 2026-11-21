import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e37-true-false', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Airbnb', 'quote': 'Frontier models return a slow, fixed true-or-false verdict'}


def check(ctx):
    s = ctx.find('airbnb', r'each model returns a verdict rather than a score, it gives a single, fixed precision-recall point')
    m = ctx.find('airbnb', r'most proprietary models return only a True or False verdict')
    if s: return ctx.ok('airbnb', s + ' … ' + (m or ''), 'said of proprietary generative models; elsewhere "most proprietary models"')
    return ctx.need('airbnb', m, 'only the "most proprietary models" wording found')


if __name__ == '__main__':
    run_cli(CLAIM, check)
