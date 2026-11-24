import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e37-coding-agents-beyond-engineering', 'artifact': 'episode', 'type': 'comparison', 'story': 'Anthropic Enterprise Study', 'quote': 'Coding agents are spreading far beyond engineering'}


def check(ctx):
    return ctx.require('anthropic', r'using coding agents to bring software capabilities to nontechnical roles')


if __name__ == '__main__':
    run_cli(CLAIM, check)
