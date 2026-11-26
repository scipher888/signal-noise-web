import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe8-factoring-verification', 'artifact': 'episode', 'type': 'objection', 'story': 'Google papers', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'no independent verification is reported')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:factoring (?:papers|results|bounds)|Google.s (?:public )?(?:papers|results)|six papers).{0,200}(?:not independently verified|no independent verification|remain unverified|unverified for now|leaving them unverified)') else ctx.fail('framing', q, 'Flag the public factoring results, not just the separate rumor, as lacking independent verification.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
