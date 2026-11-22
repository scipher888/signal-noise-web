import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e24-beam-nearly-twice-rl', 'artifact': 'episode', 'type': 'comparison', 'story': 'Nathan Lambert Cornell talk', 'quote': 'nearly twice as much for Beam'}


def check(ctx):
    return ctx.require('lambert', r'Beam Oct 2026', r'> 1\.7×')


if __name__ == '__main__':
    run_cli(CLAIM, check)
