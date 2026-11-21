import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e21-answer-keys', 'artifact': 'episode', 'type': 'attribution', 'story': 'Society', 'quote': 'code inspections still caught scripts using answer keys and leaked targets'}


def check(ctx):
    return ctx.require('society', r'code inspections found submissions in which scripts or prompts used answer keys or leaked targets')


if __name__ == '__main__':
    run_cli(CLAIM, check)
