import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e64-future-fog', 'artifact': 'episode', 'type': 'opinion', 'story': 'AI acceleration boundary', 'quote': 'until they can, every dramatic chart and every unexplained model stumble will land straight in the fog'}


def check(ctx):
    return ctx.need('bethmaybarnes', ctx.find('bethmaybarnes', r'less robust to over-interpretation'), 'Rhetorical prediction.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
