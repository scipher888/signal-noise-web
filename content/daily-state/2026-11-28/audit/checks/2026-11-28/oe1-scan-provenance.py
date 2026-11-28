import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe1-scan-provenance', 'artifact': 'episode', 'type': 'objection', 'story': 'GGUF scan', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'single-team scan, not independently replicated')
    if not ctx.art_has(r'(?is)(?:Malspark|Root0ne).{0,150}(?:scan|report|found)'): return ctx.fail('framing', q, 'Attribute the findings to the research team.')
    return ctx.ok('framing', q)


if __name__ == '__main__':
    run_cli(CLAIM, check)
