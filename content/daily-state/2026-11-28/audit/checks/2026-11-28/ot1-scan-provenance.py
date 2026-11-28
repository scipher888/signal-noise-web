import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot1-scan-provenance', 'artifact': 'takeaways', 'type': 'objection', 'story': 'GGUF scan', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'Security researcher.s primary technical report')
    if not ctx.art_has(r'(?is)(?:Malspark|Root0ne).{0,100}(?:scan|found|report)'): return ctx.fail('framing', q, 'Identify the scan team.')
    return ctx.ok('framing', q)


if __name__ == '__main__':
    run_cli(CLAIM, check)
