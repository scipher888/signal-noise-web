import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe3-no-audit', 'artifact': 'episode', 'type': 'objection', 'story': 'Anthropic capability limits', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'not independently audited')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:not|never) independently (?:audited|verified|tested)|no independent (?:audit|verification|test)') else ctx.fail('framing', q, 'Disclose lack of independent audit of the limits.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
