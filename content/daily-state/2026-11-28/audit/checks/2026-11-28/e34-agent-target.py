import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e34-agent-target', 'artifact': 'episode', 'type': 'attribution', 'story': 'timdedid', 'quote': 'A second campaign, timdedid, aimed directly at coding agents'}


def check(ctx):
    return ctx.require('gguf', r'Campaign 2: timdedid, Hijacking Coding Agents')


if __name__ == '__main__':
    run_cli(CLAIM, check)
