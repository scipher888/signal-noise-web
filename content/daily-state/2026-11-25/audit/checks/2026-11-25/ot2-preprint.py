import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot2-preprint', 'artifact': 'takeaways', 'type': 'objection', 'story': 'GPT-6 protein binders', 'quote': None}


def check(ctx):
    q = ctx.find('framing', r'Company-reported preprint')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:protein.design|OpenAI).{0,48}preprint|preprint.{0,32}OpenAI') else ctx.fail('framing', q, 'Identify the protein preprint.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
