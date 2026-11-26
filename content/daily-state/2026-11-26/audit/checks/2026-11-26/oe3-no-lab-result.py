import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe3-no-lab-result', 'artifact': 'episode', 'type': 'objection', 'story': 'Factoring rumor', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'No lab has published or confirmed such a result')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:no|neither) (?:frontier )?labs?.{0,50}(?:published|confirmed)|no lab confirmation|not confirmed by (?:either|any) lab') else ctx.fail('framing', q, 'Say that no lab has published or confirmed the rumored result.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
