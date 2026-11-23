import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe1-openai-company-reported', 'artifact': 'episode', 'type': 'objection', 'story': 'OpenAI Perplexity', 'quote': None}


def check(ctx):
    s = ctx.find('framing', r'Company-authored proposal.*internal-codebase measurements')
    if ctx.art_has(r'internal codebase|company[- ]reported|self[- ]reported|not independently reproduc'):
        return ctx.ok('framing', s, 'Episode notes OpenAI numbers are from its own internal codebase / company-reported')
    return ctx.fail('framing', s, 'Episode omits caveat that OpenAI measurements are company-reported / internal-codebase and not independently reproducible')


if __name__ == '__main__':
    run_cli(CLAIM, check)
