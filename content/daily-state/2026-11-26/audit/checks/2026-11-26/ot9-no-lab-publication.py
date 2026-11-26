import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot9-no-lab-publication', 'artifact': 'takeaways', 'type': 'objection', 'story': 'RSA rumors', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'No lab has published or confirmed such a result')
    p = r'(?:no (?:frontier )?labs? (?:has |have )?(?:publicly )?published|unpublished (?:crypto|factoring|RSA)|unreleased cryptogra\w* (?:results|bombshells))'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'State the rumored result is unpublished.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
