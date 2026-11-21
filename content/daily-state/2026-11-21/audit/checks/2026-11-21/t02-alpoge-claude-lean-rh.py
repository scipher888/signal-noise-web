import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't02-alpoge-claude-lean-rh', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Riemann Hypothesis proof claim', 'quote': 'Levent Alpöge claimed he and Claude found a Lean-formalized proof of the Riemann Hypothesis'}


def check(ctx):
    s1 = ctx.find('alpoge', r'working with Claude, discovered a proof')
    s2 = ctx.find('alpoge', r'formalized the arguments')
    s3 = ctx.find('andrewcurran_', r'Levent Alpöge')
    if s1 and s2 and s3:
        return ctx.ok('alpoge', s1, 'Author name confirmed via andrewcurran_ and Lean formalization via alpoge')
    return ctx.need('alpoge', s1 or s2, 'Could not verify author, proof claim, and Lean formalization')


if __name__ == '__main__':
    run_cli(CLAIM, check)
