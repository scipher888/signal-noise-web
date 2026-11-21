import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e26-theater', 'artifact': 'episode', 'type': 'opinion', 'story': 'Society', 'quote': 'Without an execution path, AI science risks becoming very polite, rigorous-sounding theater'}


def check(ctx):
    s = ctx.find('society', r'Evidence Needs an Execution Path')
    return ctx.need('society', s, 'opinion; echoes the paper section title quoted')


if __name__ == '__main__':
    run_cli(CLAIM, check)
