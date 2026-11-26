import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e80-thanksgiving-quote', 'artifact': 'episode', 'type': 'quote', 'story': 'Aaronson Thanksgiving advice', 'quote': 'spend Thanksgiving with the people you love'}


def check(ctx):
    return ctx.require('framing', r'\bspend Thanksgiving with the people you love\b', note='Need Aaronson’s actual wording; no quotation from the Thanksgiving passage supplied.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
