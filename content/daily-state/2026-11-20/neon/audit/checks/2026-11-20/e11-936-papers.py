import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e11-936-papers', 'artifact': 'episode', 'type': 'number', 'story': 'Society', 'quote': 'published 936 papers with code and data'}


def check(ctx):
    return ctx.require('society', r'producing 936 papers alongside their code, data')


if __name__ == '__main__':
    run_cli(CLAIM, check)
