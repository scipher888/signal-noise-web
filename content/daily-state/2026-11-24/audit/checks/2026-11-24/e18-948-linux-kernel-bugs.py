import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e18-948-linux-kernel-bugs', 'artifact': 'episode', 'type': 'number', 'story': 'Linux Cybersecurity', 'quote': '948 Linux kernel local privilege escalation bugs'}


def check(ctx):
    return ctx.require('openai2', r'948 Linux kernel bugs that could grant local root access')


if __name__ == '__main__':
    run_cli(CLAIM, check)
