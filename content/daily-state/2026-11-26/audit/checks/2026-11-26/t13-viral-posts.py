import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't13-viral-posts', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'RSA rumors', 'quote': 'Viral X posts'}


def check(ctx):
    return ctx.need('andrewcurran_', ctx.find('andrewcurran_', r'rumors are real and circulating widely'), 'A reply describes rumor circulation, not reach metrics for these posts.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
