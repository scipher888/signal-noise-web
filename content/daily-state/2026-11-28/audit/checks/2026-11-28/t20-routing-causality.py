import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't20-routing-causality', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Benchmarks and builder reports', 'quote': 'pushing many builders to supervise it with rival models or default to Sol 6.2'}


def check(ctx):
    q = ctx.find('thezvi', r'Use it as a sub-agent of another frontier AI you like using')
    if q and ctx.absent('thezvi', r'(?:many builders|many practitioners).*because.*(?:intent|reward hack)'): return ctx.fail('thezvi', q, 'Individual recommendations and preferences do not establish a widespread causal shift.')
    return ctx.require('thezvi', r'(?:many builders|many practitioners).*(?:supervis|Sol).*because.*(?:intent|reward hack)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
