import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't06-no-quantum-computer-today-qubits', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Google DeepMind quantum circuits', 'quote': 'no quantum computer today can run the hundreds to thousands of error-corrected qubits they require'}


def check(ctx):
    return ctx.require('deepmind', r"today's small quantum processors", r'4,338 error-corrected qubits', r'481 to 333 qubits')


if __name__ == '__main__':
    run_cli(CLAIM, check)
