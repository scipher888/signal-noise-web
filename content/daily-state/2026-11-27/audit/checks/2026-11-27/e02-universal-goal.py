import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e02-universal-goal', 'artifact': 'episode', 'type': 'opinion', 'story': 'AI acceleration boundary', 'quote': 'Everyone watching frontier AI wants to draw one crisp line: the point where AI systems start accelerating the work of building better AI systems.'}


def check(ctx):
    return ctx.need('metr', ctx.find('metr', r'prospect of AI R&D acceleration'), 'Editorial generalization about what everyone wants.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
