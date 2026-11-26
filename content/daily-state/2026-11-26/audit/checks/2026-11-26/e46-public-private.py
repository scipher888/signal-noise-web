import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e46-public-private', 'artifact': 'episode', 'type': 'opinion', 'story': 'RSA rumors', 'quote': 'it helps to separate public math from private rumor'}


def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'only what he says he has heard'), 'Editorial advice.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
