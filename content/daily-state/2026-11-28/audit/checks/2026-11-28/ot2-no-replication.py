import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot2-no-replication', 'artifact': 'takeaways', 'type': 'objection', 'story': 'GGUF scan', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'single-team scan, not independently replicated')
    if not ctx.art_has(r'(?is)single[- ]team scan|(?:Malspark|scan|findings).{0,160}(?:not (?:been )?independently (?:replicated|confirmed)|no independent replication)'): return ctx.fail('framing', q, 'Disclose that the scan was not independently replicated.')
    return ctx.ok('framing', q)


if __name__ == '__main__':
    run_cli(CLAIM, check)
