import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e42-access-interlock', 'artifact': 'episode', 'type': 'qualifier', 'story': 'MCP safeguards', 'quote': 'turn off automatically whenever remote or LAN access is enabled'}


def check(ctx):
    return ctx.require('unsloth', r'they turn off while Remote access or LAN access is on')


if __name__ == '__main__':
    run_cli(CLAIM, check)
