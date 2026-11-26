import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot4-lean-pending', 'artifact': 'takeaways', 'type': 'objection', 'story': 'Cogentic papers', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'announced Lean formalizations are not yet released')
    p = r'(?:Lean[^.!?]{0,100}(?:unreleased|not (?:yet )?(?:been )?released)|(?:not (?:yet )?released|unreleased)[^.!?]{0,100}Lean)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'State that the Lean artifacts are not yet released.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
