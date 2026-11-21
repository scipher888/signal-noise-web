import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e17-novelty', 'artifact': 'episode', 'type': 'comparison', 'story': 'Society', 'quote': 'humans won on novelty and significance'}


def check(ctx):
    return ctx.require('society', r'Human papers scored higher on novelty and significance')


if __name__ == '__main__':
    run_cli(CLAIM, check)
