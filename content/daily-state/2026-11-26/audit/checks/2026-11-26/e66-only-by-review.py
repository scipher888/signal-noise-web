import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e66-only-by-review', 'artifact': 'episode', 'type': 'attribution', 'story': 'Engineering oversight', 'quote': 'Anthropic succeeded only by keeping engineers at the pull-request gate and turning recurring corrections into standing rules, tests, and lints'}


def check(ctx):
    q = ctx.find('anthropic', r'human review was an important gate')
    return ctx.fail('anthropic', q, 'Important is not a finding of exclusive causal necessity.') if q and ctx.absent('anthropic', r'(?:only succeeded|succeeded only)') else ctx.require('anthropic', r'(?:only succeeded|succeeded only).{0,100}review', r'recurring problems and proposed rules', r'new tests.{0,100}lints')


if __name__ == '__main__':
    run_cli(CLAIM, check)
