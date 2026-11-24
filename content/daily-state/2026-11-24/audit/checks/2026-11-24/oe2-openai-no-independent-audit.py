import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe2-openai-no-independent-audit', 'artifact': 'episode', 'type': 'objection', 'story': 'Linux Cybersecurity', 'quote': None}


def check(ctx):
    s = ctx.find('framing', r'no independent evaluation yet|not independently audited')
    if not ctx.art_has(r'(?:company[- ]reported|self[- ]reported|not independently|no independent|unverified|OpenAI.s own (?:counts|figures|numbers))'):
        return ctx.fail('framing', s, 'Episode omits caveat that OpenAI/Cisco Shirudo and GPT-6 Cyber results are company-reported with no independent evaluation or audit')
    return ctx.ok('framing', s)


if __name__ == '__main__':
    run_cli(CLAIM, check)
