import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe12-company-metrics', 'artifact': 'episode', 'type': 'objection', 'story': 'Rust migration', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'performance numbers are Anthropic.s own')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:according to Anthropic|Anthropic (?:reports|says)|company[- ]reported).{0,200}CPU') else ctx.fail('framing', q, 'Attribute the measurements to Anthropic.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
