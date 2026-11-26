import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot2-preprint-status', 'artifact': 'takeaways', 'type': 'objection', 'story': 'Cogentic papers', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'Company-posted preprints in a public repository')
    return ctx.ok('framing', q) if ctx.art_has(r'\bpreprints?\b') else ctx.fail('framing', q, 'State preprint status.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
