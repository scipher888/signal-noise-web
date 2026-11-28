import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e39-fake-directive', 'artifact': 'episode', 'type': 'attribution', 'story': 'timdedid', 'quote': 'the template injects a fake system directive ordering an agent with shell access to download and run a remote PowerShell script from a WordPress site'}


def check(ctx):
    return ctx.require('gguf', r'fake \[SYSTEM DIRECTIVE\] that orders an agent with shell access to download and run a script', r'its powershell tool, download .* from a WordPress site .* and run it')


if __name__ == '__main__':
    run_cli(CLAIM, check)
