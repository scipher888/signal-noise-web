import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe2-inkling-company-reported', 'artifact': 'episode', 'type': 'objection', 'story': 'Inkling 2 Mini', 'quote': None}


def check(ctx):
    s = ctx.find('framing', r'Company-reported architecture and benchmark results')
    if ctx.art_has(r'(?:company[- ]reported|self[- ]reported|according to Thinking Machines|Thinking Machines(?:\'s)? (?:own |reported )?(?:benchmarks|numbers|results)|not independently (?:verified|replicated))'):
        return ctx.ok('framing', s, 'Episode carries company-reported caveat for Inkling 2 Mini')
    return ctx.fail('framing', s, 'Episode omits caveat that Inkling 2 Mini benchmarks are company-reported without independent replication')


if __name__ == '__main__':
    run_cli(CLAIM, check)
