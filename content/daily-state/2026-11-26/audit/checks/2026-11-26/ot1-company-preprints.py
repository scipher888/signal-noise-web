import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot1-company-preprints', 'artifact': 'takeaways', 'type': 'objection', 'story': 'Gemini math papers', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'Company-posted preprints in a public repository')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:Google(?: Research)?|company)[- ](?:posted|published|released).{0,100}preprints?') else ctx.fail('framing', q, 'Identify the company-posted preprints.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
