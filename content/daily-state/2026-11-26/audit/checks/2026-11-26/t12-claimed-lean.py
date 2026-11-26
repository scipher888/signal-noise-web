import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't12-claimed-lean', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Cogentic papers', 'quote': 'claimed Lean 4 formalizations'}


def check(ctx):
    q = ctx.find('google', r'Lean 4[\s\S]*entire proof has also been completed')
    if not q: return ctx.need('google', None, 'Need versioned company claim.')
    return ctx.require('framing', r'announced Lean formalizations are not yet released', note=q)


if __name__ == '__main__':
    run_cli(CLAIM, check)
