import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot1-company-reported', 'artifact': 'takeaways', 'type': 'objection', 'story': 'Cogentic papers', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'Company-posted preprints in a public repository')
    p = r'(?:Google(?: Research)? (?:says|reports|claims)|company[- ]reported|according to Google|it says its Cogentic harness)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'Identify company reporting.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
