import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe6-lean-release', 'artifact': 'episode', 'type': 'objection', 'story': 'Proof verification', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'announced Lean formalizations are not yet released')
    return ctx.ok('framing', q) if ctx.art_has(r'Lean(?: 4)? formalizations?.{0,60}(?:not yet (?:public|released)|unreleased|coming in a companion submission|will be released)|pending (?:release of (?:the )?)?Lean 4 formalizations') else ctx.fail('framing', q, 'State that the announced formalizations are not public yet.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
