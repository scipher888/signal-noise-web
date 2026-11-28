import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't08-combined', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'GGUF scan', 'quote': 'combined downloads'}


def check(ctx):
    return ctx.require('gguf', r'five malicious models downloaded 2428 times', r'Total2 actors2428')


if __name__ == '__main__':
    run_cli(CLAIM, check)
