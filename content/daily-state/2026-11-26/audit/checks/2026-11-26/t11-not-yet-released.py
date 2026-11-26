import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't11-not-yet-released', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Cogentic papers', 'quote': 'not yet released'}


def check(ctx):
    return ctx.require('framing', r'announced Lean formalizations are not yet released')


if __name__ == '__main__':
    run_cli(CLAIM, check)
