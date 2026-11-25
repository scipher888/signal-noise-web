import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e45-binding-not-medicine', 'artifact': 'episode', 'type': 'comparison', 'story': 'Protein design', 'quote': 'early lab binding is far from a working medicine'}


def check(ctx):
    return ctx.require('openai', r'binding is only one step toward a useful research tool or medicine', r'Further work would need to establish.*safety and efficacy for therapeutic applications')


if __name__ == '__main__':
    run_cli(CLAIM, check)
