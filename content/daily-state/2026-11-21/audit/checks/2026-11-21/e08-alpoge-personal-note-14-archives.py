import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e08-alpoge-personal-note-14-archives', 'artifact': 'episode', 'type': 'attribution', 'story': 'Riemann Hypothesis proof', 'quote': 'Levent Alpöge, a mathematician at Anthropic, posted a personal note along with fourteen archives of Lean code'}


def check(ctx):
    s1 = ctx.find('alpoge', r'lean\.tar\.gz\.part01.*part14')
    s2 = ctx.find('andrewcurran_', r'Levent Alpöge at Anthropic')
    if s1 and s2:
        return ctx.ok('alpoge', s1, 'Anthropic affiliation confirmed via andrewcurran_')
    return ctx.need('alpoge', s1 or s2, 'Could not verify both 14 Lean archive parts and Anthropic affiliation')


if __name__ == '__main__':
    run_cli(CLAIM, check)
