import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe4-anthropic-nonrepresentative-sample', 'artifact': 'episode', 'type': 'objection', 'story': 'Anthropic Enterprise Study', 'quote': None}


def check(ctx):
    s = ctx.find('framing', r'not a representative sample')
    if not (ctx.art_has(r'own (?:business|enterprise) customers') and ctx.art_has(r'(?:not (?:a )?representative|non-representative|qualitative)')):
        return ctx.fail('framing', s, 'Episode omits caveat that Anthropic study consists of qualitative interviews with its own customers and is not a representative sample')
    return ctx.ok('framing', s)


if __name__ == '__main__':
    run_cli(CLAIM, check)
