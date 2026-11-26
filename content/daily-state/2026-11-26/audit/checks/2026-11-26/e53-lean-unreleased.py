import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e53-lean-unreleased', 'artifact': 'episode', 'type': 'attribution', 'story': 'Google formalizations', 'quote': 'Google has not yet released the companion Lean 4 formalizations'}


def check(ctx):
    q = ctx.find('google', r'Lean 4[\s\S]*released in a companion\s+submission')
    if not q: return ctx.need('google', None, 'Need Lean version and companion release plan.')
    return ctx.require('framing', r'Google Research .*announced Lean formalizations are not yet released', note=q)


if __name__ == '__main__':
    run_cli(CLAIM, check)
