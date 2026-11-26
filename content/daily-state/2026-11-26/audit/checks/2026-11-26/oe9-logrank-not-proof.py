import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe9-logrank-not-proof', 'artifact': 'episode', 'type': 'objection', 'story': 'Google papers', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'not a proof of the conjecture')
    p = r'(?:not (?:a proof of|prove|resolve|settle)|falls short of (?:proving|resolving)) (?:the )?(?:log.rank )?conjecture|log.rank conjecture (?:remains open|is still open)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'Distinguish improving a bound from proving the conjecture.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
