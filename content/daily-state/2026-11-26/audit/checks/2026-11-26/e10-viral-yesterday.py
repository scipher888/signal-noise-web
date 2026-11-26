import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e10-viral-yesterday', 'artifact': 'episode', 'type': 'attribution', 'story': 'Math proofs', 'quote': 'Yesterday, computer scientist Scott Aaronson summed up the shock in a viral post'}


def check(ctx):
    return ctx.need('andrewcurran_', ctx.find('andrewcurran_', r'Scott Aaronson on his blog'), 'Blog mention does not establish date, contents and reach.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
