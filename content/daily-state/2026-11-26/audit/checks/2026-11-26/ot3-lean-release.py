import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot3-lean-release', 'artifact': 'takeaways', 'type': 'objection', 'story': 'Gemini math papers', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'formalizations are not yet released')
    return ctx.ok('framing', q) if ctx.art_has(r'Lean(?: 4)? formalizations?.{0,60}(?:not yet (?:public|released)|unreleased|coming in a companion submission|will be released)|pending (?:public )?release of (?:the )?Lean 4 formalizations|pending Lean 4 formalizations') else ctx.fail('framing', q, 'Specify pending release rather than implying formalization has not been done.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
