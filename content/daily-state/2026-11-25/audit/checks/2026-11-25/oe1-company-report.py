import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe1-company-report', 'artifact': 'episode', 'type': 'objection', 'story': 'Protein design', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'Company-reported preprint')
    return ctx.ok('framing', q) if ctx.art_has(r'OpenAI (?:itself )?(?:reports|says)|OpenAI.s own.{0,24}preprint|company-reported.{0,24}(?:protein|preprint)') else ctx.fail('framing', q, 'Attribute the protein results to OpenAI itself.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
