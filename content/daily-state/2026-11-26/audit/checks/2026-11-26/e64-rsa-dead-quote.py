import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e64-rsa-dead-quote', 'artifact': 'episode', 'type': 'quote', 'story': 'RSA rumors', 'quote': 'RSA was dead'}


def check(ctx):
    for a in ('andrewcurran_', 'kimmonismus'):
        q = ctx.find(a, r'\bRSA was dead\b')
        if q: return ctx.ok(a, q)
    return ctx.fail('andrewcurran_', ctx.find('andrewcurran_', r'This would crack RSA'), 'Neither supplied post uses the quoted words.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
