import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e34-unverified-now', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Proof verification', 'quote': 'leaving them unverified for now'}


def check(ctx):
    q = ctx.find('google', r'entire proof has also been completed and will be released')
    if q and not ctx.art_has(r'not independently verified|not yet independently verified|no independent verification|unverified for now|remain unverified|leaving them unverified'): return ctx.fail('google', q, 'Unreleased is not unformalized; distinguish lack of independent verification.')
    return ctx.require('framing', r'announced Lean formalizations are not yet released', r'no independent verification is reported')


if __name__ == '__main__':
    run_cli(CLAIM, check)
