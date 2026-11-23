import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe3-lingsante-company-reported', 'artifact': 'episode', 'type': 'objection', 'story': 'Ant Group LingSante', 'quote': None}


def check(ctx):
    s = ctx.find('framing', r'benchmark results are company-reported and not independently reproduced')
    if ctx.art_has(r'self[- ]reported|company[- ]reported|vendor[- ]reported|not independently (?:reproduc|verif)'):
        return ctx.ok('framing', s, 'Episode notes LingSante benchmark results are self-reported')
    return ctx.fail('framing', s, 'Episode omits caveat that LingSante benchmark results are company-reported / not independently reproduced')


if __name__ == '__main__':
    run_cli(CLAIM, check)
