import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot3-tool-provenance', 'artifact': 'takeaways', 'type': 'objection', 'story': 'GGUF scan', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'scanner and sanitizer repository published by the Malspark author')
    if not ctx.art_has(r'(?is)(?:Root0ne|Malspark|(?:same |the )researcher) (?:also )?(?:released|published|created).{0,100}gguf-radar|(?:Root0ne|Malspark)[’\x27]s (?:own )?(?:open-source )?scanner'): return ctx.fail('framing', q, 'State that the scanner came from the report author.')
    return ctx.ok('framing', q)


if __name__ == '__main__':
    run_cli(CLAIM, check)
