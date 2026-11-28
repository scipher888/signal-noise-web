import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe2-no-replication', 'artifact': 'episode', 'type': 'objection', 'story': 'GGUF scan', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'single-team scan, not independently replicated')
    if not ctx.art_has(r'(?is)(?:scan|Malspark|findings).{0,160}(?:not (?:been )?independently (?:replicated|confirmed)|no independent replication)|single[- ]team scan'): return ctx.fail('framing', q, 'Disclose the single-team evidence base.')
    return ctx.ok('framing', q)


if __name__ == '__main__':
    run_cli(CLAIM, check)
