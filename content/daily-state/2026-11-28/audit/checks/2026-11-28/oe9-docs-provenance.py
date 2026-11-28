import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe9-docs-provenance', 'artifact': 'episode', 'type': 'objection', 'story': 'MCP safeguards', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'First-party technical documentation detailing local MCP ports')
    if not ctx.art_has(r'Unsloth(?:[’\x27]s)? (?:own )?(?:MCP |technical )?(?:documentation|docs|guide)'): return ctx.fail('framing', q, 'Identify the app restrictions as vendor-documented.')
    return ctx.ok('framing', q)


if __name__ == '__main__':
    run_cli(CLAIM, check)
