import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't08-two-factoring-results', 'artifact': 'takeaways', 'type': 'number', 'story': 'Cogentic papers', 'quote': 'two integer factoring results'}


def check(ctx):
    return ctx.require('framing', r'(?:two|2) (?:new )?(?:integer factoring results|results on integer factoring)', note='Overall count six does not establish this subtotal.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
