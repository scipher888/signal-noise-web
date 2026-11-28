import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e41-app-execution', 'artifact': 'episode', 'type': 'attribution', 'story': 'MCP safeguards', 'quote': "Unsloth's own MCP documentation warns that local app bridges execute code inside your software"}


def check(ctx):
    return ctx.require('unsloth', r'These tools run code in your app, so only the owner account can use them')


if __name__ == '__main__':
    run_cli(CLAIM, check)
