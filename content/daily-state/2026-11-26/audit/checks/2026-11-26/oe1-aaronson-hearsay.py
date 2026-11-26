import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe1-aaronson-hearsay', 'artifact': 'episode', 'type': 'objection', 'story': 'Factoring rumor', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'only what he says he has heard')
    return ctx.ok('framing', q) if ctx.art_has(r'Aaronson.{0,100}(?:heard|told|from multiple reliable sources)') else ctx.fail('framing', q, 'Identify the information as second hand.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
