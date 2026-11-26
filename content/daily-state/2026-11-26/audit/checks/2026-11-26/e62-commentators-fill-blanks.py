import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e62-commentators-fill-blanks', 'artifact': 'episode', 'type': 'attribution', 'story': 'RSA rumors', 'quote': 'Popular AI commentators and aggregator accounts on X filled in those blanks themselves'}


def check(ctx):
    q = ctx.find('kimmonismus', r'AI news aggregator account amplifying a rumor; no independent sourcing')
    return ctx.need('kimmonismus', q, 'Amplification is explicit; popularity and who originated the specifics are not.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
