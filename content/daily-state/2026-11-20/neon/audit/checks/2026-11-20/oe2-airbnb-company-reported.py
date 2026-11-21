import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe2-airbnb-company-reported', 'artifact': 'episode', 'type': 'objection', 'story': 'Airbnb', 'quote': None}


def check(ctx):
    # Objection: Airbnb result is company-reported, on its own data, for one task
    s = ctx.find('framing', r'Company-reported benchmark on Airbnb.s own held-out data for one production task')
    if not s: return ctx.ok(None, None, 'no such caveat in the scan framing for this story')
    if ctx.art_has(r"company[- ]reported|airbnb (says|reports|reported|claims)|according to airbnb|airbnb's own (data|benchmark|test)|its own (held-out )?data|(one|single) (production )?(task|classifier)"): return ctx.ok('framing', s, 'caveat present in artifact')
    return ctx.fail('framing', s, 'artifact never states this caveat (Airbnb result is company-reported, on its own data, for one task)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
