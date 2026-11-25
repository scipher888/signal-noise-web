import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe7-historian-account', 'artifact': 'episode', 'type': 'objection', 'story': 'Chabot sketchbook', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'Single historian.s first-person account')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:historian Mark Humphries|Humphries).{0,36}(?:describes|reports|recounts|says|writes)|Humphries.s (?:own |first-person )?account') else ctx.fail('framing', q, 'Frame the attribution as the historian’s account.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
