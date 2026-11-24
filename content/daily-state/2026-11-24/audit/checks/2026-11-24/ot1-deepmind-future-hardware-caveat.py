import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'ot1-deepmind-future-hardware-caveat', 'artifact': 'takeaways', 'type': 'objection', 'story': 'Google DeepMind quantum circuits', 'quote': None}


def check(ctx):
    s = ctx.find('framing', r'resource savings are estimates for hardware that does not exist yet')
    if not ctx.art_has(r'(?:hardware that does not exist|future hardware|no quantum computer.*today|cannot run.*today)'):
        return ctx.fail('framing', s, 'Takeaways omit caveat that quantum circuit savings are estimates for hardware that does not exist yet')
    return ctx.ok('framing', s, 'Takeaways note that no quantum computer today can run these circuits')


if __name__ == '__main__':
    run_cli(CLAIM, check)
