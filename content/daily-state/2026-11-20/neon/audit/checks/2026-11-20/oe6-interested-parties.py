import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe6-interested-parties', 'artifact': 'episode', 'type': 'objection', 'story': 'Airbnb/Blueprint', 'quote': None}


def check(ctx):
    # Objection: promoters with a stake (Google's Gemma account, OpenAI's president) must be identified as such.
    g = ctx.art_has(r"Google's Gemma account"); b = ctx.art_has(r"OpenAI's Greg Brockman")
    s = ctx.find('framing', r'Company-reported')
    return ctx.ok(None, None, 'both promoters identified with their company') if g and b else ctx.fail(None, None, f'gemma identified={g}, brockman identified={b}')


if __name__ == '__main__':
    run_cli(CLAIM, check)
