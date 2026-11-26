import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e66-same-house', 'artifact': 'episode', 'type': 'comparison', 'story': 'Dual-use mathematics', 'quote': 'In theoretical computer science, lower bounds and algorithms live in the same house'}


def check(ctx):
    return ctx.need(None, None, 'Disciplinary metaphor, not a literal source comparison.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
