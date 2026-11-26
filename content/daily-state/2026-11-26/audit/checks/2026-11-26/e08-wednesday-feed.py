import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e08-wednesday-feed', 'artifact': 'episode', 'type': 'opinion', 'story': 'RSA rumors', 'quote': 'by Wednesday afternoon, if you opened X, you would barely know anyone had proven anything in pure math'}


def check(ctx):
    return ctx.need('kimmonismus', ctx.find('kimmonismus', r'AI news aggregator account amplifying a rumor'), 'A post cannot establish the experience of a typical X reader.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
