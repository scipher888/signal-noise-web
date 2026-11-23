import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot3-lingsante-company-reported', 'artifact': 'takeaways', 'type': 'objection', 'story': 'Ant Group LingSante-3.1-flash', 'quote': None}


def check(ctx):
    s = ctx.find('framing', r'benchmark results are company-reported and not independently reproduced')
    if ctx.art_has(r'self[- ]reported|company[- ]reported|vendor[- ]reported|not independently (?:reproduc|verif)'):
        return ctx.ok('framing', s, 'Takeaways note LingSante benchmark results are self-reported')
    return ctx.fail('framing', s, 'Takeaways omit caveat that LingSante benchmark results are company-reported / not independently reproduced')


if __name__ == '__main__':
    run_cli(CLAIM, check)
