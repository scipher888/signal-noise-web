import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'oe1-deepmind-future-hardware-caveat', 'artifact': 'episode', 'type': 'objection', 'story': 'Quantum Circuits', 'quote': None}


def check(ctx):
    s = ctx.find('framing', r'resource savings are estimates for hardware that does not exist yet')
    if not ctx.art_has(r'(?:hardware that does not exist|future hardware|no quantum computer.*today|cannot run.*today)'):
        return ctx.fail('framing', s, 'Episode omits caveat that quantum circuit savings are estimates for hardware that does not exist yet')
    return ctx.ok('framing', s, 'Episode notes that quantum circuit savings are for future hardware / no quantum computer can run them today')


if __name__ == '__main__':
    run_cli(CLAIM, check)
