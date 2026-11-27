import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe9-company-loss', 'artifact': 'episode', 'type': 'objection', 'story': 'OpenAI loss curve', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'company-reported OpenAI loss data')
    return ctx.ok('framing', q) if ctx.art_has(r'OpenAI (?:recently )?(?:published|reported|released)[^.]{0,70}(?:loss|data)|OpenAI.s (?:own |published |reported )?(?:numbers|data)') else ctx.fail('framing', q, 'Identify OpenAI as the source of the measurements.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
