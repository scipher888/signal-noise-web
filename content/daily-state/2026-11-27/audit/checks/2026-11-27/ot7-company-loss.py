import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot7-company-loss', 'artifact': 'takeaways', 'type': 'objection', 'story': 'Pretraining loss', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'company-reported OpenAI loss data')
    return ctx.ok('framing', q) if ctx.art_has(r'OpenAI.s (?:own |published |reported )?(?:numbers|data)|OpenAI (?:published|reported|released)[^.]{0,70}(?:loss|data)') else ctx.fail('framing', q, 'Attribute underlying data to OpenAI.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
