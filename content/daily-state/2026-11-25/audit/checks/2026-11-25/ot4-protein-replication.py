import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot4-protein-replication', 'artifact': 'takeaways', 'type': 'objection', 'story': 'GPT-6 protein binders', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'Onava; no independent replication')
    return ctx.ok('framing', q) if ctx.art_has(r'(?is)(?:Onava|binder|protein|OpenAI reports).{0,200}(?:no independent replication|not (?:yet )?independently replicated|hasn.t been independently replicated)|(?:no independent replication|not independently replicated).{0,80}(?:protein|binder)') else ctx.fail('framing', q, 'Disclose no independent replication of binding results.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
