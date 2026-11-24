import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e02-deepmind-quantum-attribution', 'artifact': 'episode', 'type': 'attribution', 'story': 'Quantum Circuits', 'quote': 'Google DeepMind and Google Quantum AI announced that teams of Gemini 4 agents discovered significantly cheaper quantum circuits for future hardware'}


def check(ctx):
    return ctx.require('deepmind', r'collaboration between Google DeepMind and Google Quantum AI', r'teams of Gemini 4 agents.*quantum circuits')


if __name__ == '__main__':
    run_cli(CLAIM, check)
