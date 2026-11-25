import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe9-archival-confirmation', 'artifact': 'episode', 'type': 'objection', 'story': 'Chabot sketchbook', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'attribution rests on archival documents he obtained')
    carried = ctx.art_has(r'(?:Humphries|historian|he) (?:ordered|obtained|received).{0,40}(?:scans|diary|documents|journal)') and ctx.art_has(r'match(?:ed|ing).{0,20}handwriting|handwriting matched|took a sketch')
    return ctx.ok('framing', q) if carried else ctx.fail('framing', q, 'Identify the archival evidence the historian obtained and checked.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
