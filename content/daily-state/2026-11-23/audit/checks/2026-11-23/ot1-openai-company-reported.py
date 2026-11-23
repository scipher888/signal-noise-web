import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot1-openai-company-reported', 'artifact': 'takeaways', 'type': 'objection', 'story': 'OpenAI perplexity warning', 'quote': None}


def check(ctx):
    s = ctx.find('framing', r'Company-authored proposal.*internal-codebase measurements')
    if ctx.art_has(r'internal (?:held-out|codebase)|company[- ]reported|self[- ]reported|not independently reproduc'):
        return ctx.ok('framing', s, 'Takeaways note OpenAI internal/company-reported measurements')
    return ctx.fail('framing', s, 'Takeaways omit caveat that OpenAI measurements are company-reported / internal-codebase')


if __name__ == '__main__':
    run_cli(CLAIM, check)
