import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't01-malspark', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'GGUF scan', 'quote': 'A Malspark scan'}


def check(ctx):
    return ctx.require('framing', r'Malspark scan finds 5 GGUF malware models', r'framing \(Malspark\): Security researcher.s primary technical report')


if __name__ == '__main__':
    run_cli(CLAIM, check)
