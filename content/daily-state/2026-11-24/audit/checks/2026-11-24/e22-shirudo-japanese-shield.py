import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e22-shirudo-japanese-shield', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Linux Cybersecurity', 'quote': 'Shirudo, Japanese for shield'}


def check(ctx):
    return ctx.require('openai', r'Shirudo.*Japanese.*shield', note='Shirudo etymology not in available source snapshots')


if __name__ == '__main__':
    run_cli(CLAIM, check)
