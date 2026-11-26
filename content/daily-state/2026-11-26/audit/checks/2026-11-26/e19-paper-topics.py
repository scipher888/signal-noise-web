import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e19-paper-topics', 'artifact': 'episode', 'type': 'attribution', 'story': 'Google papers', 'quote': 'They cover integer factoring, discrete logarithms, the log-rank conjecture, approximate Nash equilibria, and graph edge reconstruction'}


def check(ctx):
    return ctx.require('framing', r'papers.{0,100}factoring, the log-rank conjecture', r'discrete logarithms', r'approximate Nash equilibria', r'graph edge reconstruction')


if __name__ == '__main__':
    run_cli(CLAIM, check)
