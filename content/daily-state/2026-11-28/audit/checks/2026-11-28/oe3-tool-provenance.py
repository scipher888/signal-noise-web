import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe3-tool-provenance', 'artifact': 'episode', 'type': 'objection', 'story': 'GGUF defenses', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'scanner and sanitizer repository published by the Malspark author')
    if not ctx.art_has(r'(?is)(?:Root0ne|Malspark|(?:same |the )researcher).{0,100}(?:released|published|created).{0,100}gguf-radar'): return ctx.fail('framing', q, 'Identify the tool as the report author’s own release.')
    return ctx.ok('framing', q)


if __name__ == '__main__':
    run_cli(CLAIM, check)
