import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't11-open-source', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'GGUF scan', 'quote': 'open-source scanner gguf-radar'}


def check(ctx):
    return ctx.require('gguf', r'open-source tool gguf-radar detects these templates and hidden bytes')


if __name__ == '__main__':
    run_cli(CLAIM, check)
