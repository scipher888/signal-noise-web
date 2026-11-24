import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e13-open-sourced-lean-library', 'artifact': 'episode', 'type': 'attribution', 'story': 'Quantum Circuits', 'quote': 'DeepMind open-sourced the Lean library and proofs for outside checking'}


def check(ctx):
    return ctx.require('deepmind', r'open-sourcing our Lean library, problem specifications, and verified solutions')


if __name__ == '__main__':
    run_cli(CLAIM, check)
