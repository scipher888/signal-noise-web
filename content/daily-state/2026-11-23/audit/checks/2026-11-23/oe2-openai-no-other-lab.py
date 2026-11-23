import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe2-openai-no-other-lab', 'artifact': 'episode', 'type': 'objection', 'story': 'OpenAI Perplexity', 'quote': None}


def check(ctx):
    s = ctx.find('framing', r'no other lab has committed')
    if ctx.art_has(r'no other lab|other labs have not|not (?:yet )?committed|unilateral'):
        return ctx.ok('framing', s, 'Episode notes that no other lab has committed to OpenAI\'s proposal')
    return ctx.fail('framing', s, 'Episode omits caveat that no other lab has committed to the proposed limits')


if __name__ == '__main__':
    run_cli(CLAIM, check)
