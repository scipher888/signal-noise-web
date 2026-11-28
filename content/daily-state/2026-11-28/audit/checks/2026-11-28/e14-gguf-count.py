import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e14-gguf-count', 'artifact': 'episode', 'type': 'number', 'story': 'GGUF scan', 'quote': 'statically inspecting more than two hundred and twenty-six thousand GGUF repositories'}


def check(ctx):
    return ctx.require('gguf', r'including 226310 GGUF repositories.*parsed 572184 chat templates statically')


if __name__ == '__main__':
    run_cli(CLAIM, check)
