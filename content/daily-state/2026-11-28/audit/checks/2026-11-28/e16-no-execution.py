import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e16-no-execution', 'artifact': 'episode', 'type': 'qualifier', 'story': 'GGUF scan', 'quote': 'without executing a single model'}


def check(ctx):
    return ctx.require('gguf', r'parsed 572184 chat templates statically, without executing any of them', r'no model was downloaded in full', r'detects these templates and hidden bytes without running anything')


if __name__ == '__main__':
    run_cli(CLAIM, check)
