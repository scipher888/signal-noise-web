import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e21-two-stages', 'artifact': 'episode', 'type': 'number', 'story': 'Mir2k', 'quote': 'used a patient two-stage trap'}


def check(ctx):
    return ctx.require('gguf', r'hidden program is uploaded first and the template is changed two to four days later')


if __name__ == '__main__':
    run_cli(CLAIM, check)
