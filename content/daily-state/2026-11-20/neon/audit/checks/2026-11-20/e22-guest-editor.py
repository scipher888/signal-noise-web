import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e22-guest-editor', 'artifact': 'episode', 'type': 'attribution', 'story': 'Society', 'quote': 'A guest editor turned referee objections into scripts and ran them on the uploaded data'}


def check(ctx):
    return ctx.require('society', r'guest editor then translated 276 objections .* into scripts that were run on the uploaded data')


if __name__ == '__main__':
    run_cli(CLAIM, check)
