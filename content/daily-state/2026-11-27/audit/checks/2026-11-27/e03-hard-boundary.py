import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e03-hard-boundary', 'artifact': 'episode', 'type': 'opinion', 'story': 'AI acceleration boundary', 'quote': 'This week showed how hard it is to locate that line, whether you are trying to measure it from the outside or fence it off inside a live product.'}


def check(ctx):
    return ctx.need('claude', ctx.find('claude', r'where the limits actually stop'), 'Interpretive link between two stories.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
