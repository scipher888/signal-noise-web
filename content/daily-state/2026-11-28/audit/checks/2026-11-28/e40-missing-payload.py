import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e40-missing-payload', 'artifact': 'episode', 'type': 'attribution', 'story': 'timdedid', 'quote': 'Malspark could not recover that second-stage payload'}


def check(ctx):
    return ctx.require('gguf', r'second-stage script was not recovered for this study')


if __name__ == '__main__':
    run_cli(CLAIM, check)
