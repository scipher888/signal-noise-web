import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe2-company-caps', 'artifact': 'episode', 'type': 'objection', 'story': 'Anthropic capability limits', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'Company-reported description of its own training-time limits')
    return ctx.ok('framing', q) if ctx.art_has(r'Anthropic(?:.s (?:disclosure|launch post)| (?:says|said|reported|disclosed|framed))[^.!?]{0,200}(?:limit|cap|training|untouched)') else ctx.fail('framing', q, 'Attribute the description of the limits to Anthropic.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
