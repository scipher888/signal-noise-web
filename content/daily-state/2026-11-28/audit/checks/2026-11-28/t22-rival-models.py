import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't22-rival-models', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Benchmarks and builder reports', 'quote': 'rival models'}


def check(ctx):
    return ctx.require('thezvi', r'different model like Neon or Opus call 6\.2 subagents', r'Works well if orchestrated by Opus')


if __name__ == '__main__':
    run_cli(CLAIM, check)
