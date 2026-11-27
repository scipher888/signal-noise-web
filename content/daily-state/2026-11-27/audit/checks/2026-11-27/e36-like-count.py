import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e36-like-count', 'artifact': 'episode', 'type': 'number', 'story': 'Claude sabotage allegations', 'quote': 'The post topped nineteen thousand likes'}


def check(ctx):
    return ctx.require('claude', r'(?:post|it) (?:passed|topped|surpassed|has passed) (?:19,000|19k|nineteen thousand) likes', note='Views and likes on replies are not likes on the original post.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
