import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e53-blog-status', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Chabot sketchbook', 'quote': 'a Substack post not yet peer-reviewed or publicly audited'}


def check(ctx):
    return ctx.require('framing', r'Single historian.s first-person account', r'no independent historian review is reported yet', note='No reported independent review; this is not a search for every possible private review.') if ctx.find('gpt62', r'Substack is the home for writing') else ctx.need('gpt62', None, 'Verify publication venue.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
